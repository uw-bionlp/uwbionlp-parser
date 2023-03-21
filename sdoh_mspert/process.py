import os
import json
import spacy

from spert import sampling
from spert.input_reader import JsonInputReader
from spert.evaluator import Evaluator
from spert import models
from spert.entities import Dataset
from spert.spert_trainer import SpERTTrainer
from transformers import BertTokenizer, BertConfig

import torch
from torch.utils.data import DataLoader

from proto.python.uwbionlp_pb2 import PredictionOutput, PredictionEvent, PredictionEventArgument

class DocumentProcessor():

    def __init__(self):
        self.model_dir = os.path.join('model','20230320')
        self.spacy     = spacy.load('en_core_web_sm')
        self.tokenizer = BertTokenizer.from_pretrained(self.model_dir, do_lower_case=False, cache_dir=None)
        self.config    = BertConfig.from_pretrained(self.model_dir, cache_dir=None)

        self.args      = Args(os.path.join(self.model_dir, 'spert_args.json'))
        self.reader    = JsonInputReader(os.path.join(self.model_dir, 'spert_types.json'), self.tokenizer,
                                         max_span_size=self.args.max_span_size, logger=None)
        model_class    = models.get_model('spert')
        self.extractor = SpERTTrainer(self.args)
        self.model     = model_class.from_pretrained(self.model_dir,
                                            config = self.config,
                                            # SpERT model parameters
                                            cls_token = self.tokenizer.convert_tokens_to_ids('[CLS]'),
                                            relation_types = self.reader.relation_type_count - 1,
                                            entity_types = self.reader.entity_type_count,
                                            subtypes = self.reader.subtype_count,
                                            sent_label_types = self.reader.sent_type_count,
                                            max_pairs = self.args.max_pairs,
                                            prop_drop = self.args.prop_drop,
                                            size_embedding = self.args.size_embedding,
                                            freeze_transformer = self.args.freeze_transformer,
                                            subtype_classification = self.args.subtype_classification,
                                            concat_sent_pred = self.args.concat_sent_pred,
                                            include_adjacent = self.args.include_adjacent,
                                            include_word_piece_task = self.args.include_word_piece_task,
                                            concat_word_piece_logits = self.args.concat_word_piece_logits,
                                            cache_dir = self.args.cache_path)

    def parse_document(self, reader, tokenizer, doc):
        dataset = Dataset(label = 'eval', rel_types = reader._relation_types, entity_types = reader._entity_types,
                        subtypes = reader._subtypes, sent_types = reader._sent_types, neg_entity_count = reader._neg_entity_count,
                        neg_rel_count = reader._neg_rel_count, max_span_size = reader._max_span_size)

        for sentence in doc.sentences:
            doc_tokens = []
            doc_encoding = [tokenizer.convert_tokens_to_ids('[CLS]')]

            for i, spacy_token in enumerate(self.spacy(sentence.text)):
                token_phrase = spacy_token.text
                token_encoding = tokenizer.encode(token_phrase, add_special_tokens=False)
                if not token_encoding:
                    token_encoding = [tokenizer.convert_tokens_to_ids('[UNK]')]
                span_start, span_end = (len(doc_encoding), len(doc_encoding) + len(token_encoding))
                token = dataset.create_token(i, span_start, span_end, token_phrase)
                doc_tokens.append(token)
                doc_encoding += token_encoding
            doc_encoding += [tokenizer.convert_tokens_to_ids('[SEP]')]

            dataset.create_document(tokens = doc_tokens, entity_mentions = [], subtype_mentions = [],
                                    relations = [], sent_labels = [0], word_piece_labels = [('None', 0)]*len(doc_encoding),
                                    doc_encoding = doc_encoding)
        
        return dataset

    def predict(self, doc, device=-1):
        dataset = self.parse_document(self.reader, self.tokenizer, doc)
        evaluator = Evaluator(dataset, self.reader, self.tokenizer,
                              self.args.rel_filter_threshold, self.args.no_overlapping, predictions_path=None,
                              examples_path=None, example_count=0)
        # create data loader
        dataset.switch_mode(Dataset.EVAL_MODE)
        data_loader = DataLoader(dataset, batch_size=1, shuffle=False, drop_last=False,
                                 num_workers=0, collate_fn=sampling.collate_fn_padding)
        
        with torch.no_grad():
            self.model.eval()

            # iterate batches
            #total = math.ceil(dataset.document_count / self.args.eval_batch_size)
            for batch in data_loader:

                # move batch to selected device
                if device != -1:
                    batch = to_device(batch, device)

                # run model (forward pass)
                result = self.model( \
                                encodings = batch['encodings'],
                                context_masks = batch['context_masks'],
                                entity_masks = batch['entity_masks'],
                                entity_masks_adj = batch['entity_masks_adj'],
                                entity_sizes = batch['entity_sizes'],
                                entity_spans = batch['entity_spans'],
                                entity_sample_masks = batch['entity_sample_masks'],
                                inference = True)
                entity_clf, subtype_clf, rel_clf, rels, sent_clf = result
    
                # evaluate batch
                evaluator.eval_batch( \
                                    batch_entity_clf = entity_clf,
                                    batch_subtype_clf = subtype_clf,
                                    batch_rel_clf = rel_clf,
                                    batch_rels = rels,
                                    batch_sent_clf = sent_clf,
                                    batch = batch)
        predictions = evaluator.store_predictions()[0]

        # Return Protobuf Result object.
        result = PredictionOutput()
        for i, entity in enumerate(predictions['entities']):

            pred_ev                 = PredictionEvent()
            pred_ev.type            = entity['type']

            # Add entity itself as arg (mainly to capture token indices)
            pred_arg                = PredictionEventArgument()
            pred_arg.type           = entity['type']
            pred_arg.char_start_idx = entity['start']
            pred_arg.char_end_idx   = entity['end']
            pred_arg.text           = ' '.join(predictions['tokens'][entity['start']:entity['end']])
            pred_ev.arguments.append(pred_arg)

            # Add subtype as arg if labeled
            subtype   = predictions['subtypes'][i]['type']
            tp, label = get_type_and_label(subtype)
            if label:
                pred_arg                = PredictionEventArgument()
                pred_arg.type           = tp if tp else ''
                pred_arg.char_start_idx = entity['start']
                pred_arg.char_end_idx   = entity['end']
                pred_arg.text           = ' '.join(predictions['tokens'][entity['start']:entity['end']])
                pred_arg.label          = label
                pred_ev.arguments.append(pred_arg)

            # Add any entities linked by relations as args
            for arg_idx in [r['tail'] for r in predictions['relations'] if r['head'] == i]:
                arg_entity  = predictions['entities'][arg_idx]
                arg_subtype = predictions['subtypes'][arg_idx]['type']

                pred_arg = PredictionEventArgument()
                tp, label               = get_type_and_label(arg_subtype)
                pred_arg.char_start_idx = arg_entity['start']
                pred_arg.char_end_idx   = arg_entity['end']
                pred_arg.type           = tp if tp and tp else arg_entity['type']
                pred_arg.text           = ' '.join(predictions['tokens'][arg_entity['start']:arg_entity['end']])
                pred_arg.label          = label
                pred_ev.arguments.append(pred_arg)
            result.predictions.append(pred_ev)

        return result

def get_type_and_label(subtypes):
    for key, value in subtypes.items():
        if value != 'None':
            return key, value
    return '', ''

def to_device(batch, device):
    converted_batch = dict()
    for key in batch.keys():
        converted_batch[key] = batch[key].to(device)

    return converted_batch

class Args:
    def __init__(self, path):
        with open(path, encoding='utf-8') as fin:
            d = json.loads(fin.read())
        for key, value in d.items():
            setattr(self, key, value)