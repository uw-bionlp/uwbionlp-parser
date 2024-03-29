import torch
from torch import nn as nn
from transformers import BertConfig
from transformers import BertModel
from transformers import BertPreTrainedModel
from collections import OrderedDict

from allennlp.modules import FeedForward
from allennlp.nn import Activation
import torch.nn.functional as F

import logging

from spert import sampling
from spert import util

NO_SUBTYPE = "no_subtype"
NO_CONCAT = "no_concat"
CONCAT_LOGITS = "concat_logits"
CONCAT_PROBS = "concat_probs"
LABEL_BIAS = "label_bias"




def get_token(h: torch.tensor, x: torch.tensor, token: int):
    """ Get specific token embedding (e.g. [CLS]) """
    emb_size = h.shape[-1]

    token_h = h.view(-1, emb_size)
    flat = x.contiguous().view(-1)

    # get contextualized embedding of given token
    token_h = token_h[flat == token, :]

    return token_h


class SpERT(BertPreTrainedModel):
    """ Span-based model to jointly extract entities and relations """

    VERSION = '1.1'

    def __init__(self, config: BertConfig, cls_token: int, relation_types: int, entity_types: int, subtypes: int, sent_label_types:int,
                 size_embedding: int, prop_drop: float, freeze_transformer: bool,  max_pairs: int = 100,
                 subtype_classification: str = CONCAT_LOGITS, 
                 concat_sent_pred: bool=False, include_adjacent: bool=False, include_word_piece_task: bool=False, concat_word_piece_logits: bool=False):
        super(SpERT, self).__init__(config)


        self.subtype_classification = subtype_classification
        self.concat_sent_pred = concat_sent_pred
        self.include_adjacent = include_adjacent
        self.include_word_piece_task = include_word_piece_task
        self.concat_word_piece_logits = concat_word_piece_logits

        # BERT model
        self.bert = BertModel(config)

        linear_activation = Activation.by_name('linear')()
        tanh_activation = Activation.by_name('tanh')()

        relation_input_dim = config.hidden_size * 3 + size_embedding * 2




        entity_input_dim = config.hidden_size * 2 + size_embedding
        if self.concat_sent_pred:
            entity_input_dim += sent_label_types
        if self.include_adjacent:
            entity_input_dim += config.hidden_size
        if self.concat_word_piece_logits:
            logging.warn(f'''Concatenating word piece logits disabled but "concat_word_piece_logits=True"''')
            #entity_input_dim += entity_types
            #relation_input_dim += entity_types*2


        subtype_input_dim = entity_input_dim
        # if self.subtype_classification in [NO_SUBTYPE, NO_CONCAT, LABEL_BIAS]:
        if self.subtype_classification in [NO_SUBTYPE, NO_CONCAT]:
            pass
        elif self.subtype_classification in [CONCAT_LOGITS, CONCAT_PROBS]:
            subtype_input_dim += entity_types
        else:
            raise ValueError(f"Invalid subtype classification: {self.subtype_classification}")


        self.rel_classifier = FeedForward( \
                                input_dim = relation_input_dim,
                                num_layers = 1,
                                hidden_dims = relation_types,
                                activations = linear_activation,
                                dropout = 0.0)
        print("relation_classifier:", self.rel_classifier)

        self.entity_classifier = FeedForward( \
                                input_dim = entity_input_dim,
                                num_layers = 1,
                                hidden_dims = entity_types,
                                activations = linear_activation,
                                dropout = 0.0)
        print("entity_classifier:", self.entity_classifier)


        self.subtype_classifiers = nn.ModuleDict()
        for layer_name, label_count in subtypes.items():

            self.subtype_classifiers[layer_name] = FeedForward( \
                                    input_dim = subtype_input_dim,
                                    num_layers = 1,
                                    hidden_dims = label_count,
                                    activations = linear_activation,
                                    dropout = 0.0)
        print("subtype_classifiers:")
        for layer_name, classifier in self.subtype_classifiers.items():
            print(f"\t\t{layer_name} - {classifier}")

        # self.subtype_bias = FeedForward( \
        #                         input_dim = entity_types,
        #                         num_layers = 1,
        #                         hidden_dims = subtypes,
        #                         activations = linear_activation,
        #                         dropout = 0.0)
        # print("subtype_bias:", self.subtype_bias)


        self.sent_classifier = FeedForward( \
                                input_dim = config.hidden_size,
                                num_layers = 1,
                                hidden_dims = sent_label_types,
                                activations = linear_activation,
                                dropout = 0.0)
        print("sent_classifier:", self.sent_classifier)

        self.word_piece_classifier = FeedForward( \
                                input_dim = config.hidden_size,
                                num_layers = 1,
                                hidden_dims = entity_types,
                                activations = linear_activation,
                                dropout = 0.0)


        #self.rel_classifier = nn.Linear(config.hidden_size * 3 + size_embedding * 2, relation_types)
        #self.entity_classifier = nn.Linear(config.hidden_size * 2 + size_embedding, entity_types)

        #self.subtype_classifier = nn.Linear(config.hidden_size * 2 + size_embedding, subtypes)



        self.size_embeddings = nn.Embedding(100, size_embedding)
        self.dropout = nn.Dropout(prop_drop)

        self._cls_token = cls_token
        self._relation_types = relation_types
        self._entity_types = entity_types
        self._subtypes = subtypes
        self._max_pairs = max_pairs

        # weight initialization
        self.init_weights()

        if freeze_transformer:
            print("Freeze transformer weights")

            # freeze all transformer weights
            for param in self.bert.parameters():
                param.requires_grad = False

    def _forward_train(self, encodings: torch.tensor, context_masks: torch.tensor, entity_masks: torch.tensor, entity_masks_adj: torch.tensor,
                       entity_sizes: torch.tensor, relations: torch.tensor, rel_masks: torch.tensor):
        # get contextualized token embeddings from last transformer layer
        context_masks = context_masks.float()
        h = self.bert(input_ids=encodings, attention_mask=context_masks)['last_hidden_state']

        batch_size = encodings.shape[0]

        # get [CLS] embedding
        cls_embedding = get_token(h, encodings, self._cls_token)

        # get sentence-level predictions
        sent_clf = self._classify_sentences(cls_embedding)

        # get_size_embeddings
        size_embeddings = self.size_embeddings(entity_sizes)  # embed entity candidate sizes

        # create entity context
        if self.concat_sent_pred:
            entity_ctx = torch.cat([cls_embedding, sent_clf], dim=1)
        else:
            entity_ctx = cls_embedding


        # word_piece_clf = None
        # word_piece_clf = self._classify_word_pieces(h, include=self.include_word_piece_task)

        # if self.concat_word_piece_logits:
        #     h_entity = torch.cat([h, word_piece_clf], dim=-1)
        # else:
        #     h_entity = h

        # classify entities
        #entity_clf, subtype_clf, entity_spans_pool = self._classify_entities(encodings, h, entity_masks, size_embeddings)
        entity_clf, subtype_clf, entity_spans_pool = self._classify_entities( \
                                            h = h,
                                            entity_masks = entity_masks,
                                            entity_masks_adj = entity_masks_adj,
                                            size_embeddings = size_embeddings,
                                            entity_ctx = entity_ctx)



        # classify relations
        h_large = h.unsqueeze(1).repeat(1, max(min(relations.shape[1], self._max_pairs), 1), 1, 1)

        rel_clf = torch.zeros([batch_size, relations.shape[1], self._relation_types]).to(
            h.device)
            # self.rel_classifier.weight.device)

        # obtain relation logits
        # chunk processing to reduce memory usage
        for i in range(0, relations.shape[1], self._max_pairs):
            # classify relation candidates
            chunk_rel_logits = self._classify_relations(entity_spans_pool, size_embeddings,
                                                        relations, rel_masks, h_large, i)
            rel_clf[:, i:i + self._max_pairs, :] = chunk_rel_logits


        # return entity_clf, subtype_clf, rel_clf, sent_clf, word_piece_clf
        return entity_clf, subtype_clf, rel_clf, sent_clf

    def _forward_inference(self, encodings: torch.tensor, context_masks: torch.tensor, entity_masks: torch.tensor, entity_masks_adj: torch.tensor,
                           entity_sizes: torch.tensor, entity_spans: torch.tensor, entity_sample_masks: torch.tensor):
        # get contextualized token embeddings from last transformer layer
        context_masks = context_masks.float()
        h = self.bert(input_ids=encodings, attention_mask=context_masks)['last_hidden_state']

        batch_size = encodings.shape[0]
        ctx_size = context_masks.shape[-1]

        # get [CLS] embedding
        cls_embedding = get_token(h, encodings, self._cls_token)

        # get sentence-level predictions
        sent_clf = self._classify_sentences(cls_embedding)

        # get_size_embeddings
        size_embeddings = self.size_embeddings(entity_sizes)  # embed entity candidate sizes

        # classify entities
        #entity_clf, subtype_clf, entity_spans_pool = self._classify_entities(encodings, h, entity_masks, size_embeddings)

        # create entity context
        if self.concat_sent_pred:
            entity_ctx = torch.cat([cls_embedding, sent_clf], dim=1)
        else:
            entity_ctx = cls_embedding


        # word_piece_clf = None
        # word_piece_clf = self._classify_word_pieces(h, include=self.include_word_piece_task)


        # if self.concat_word_piece_logits:
        #     h_entity = torch.cat([h, word_piece_clf], dim=-1)
        # else:
        #     h_entity = h

        # classify entities
        #entity_clf, subtype_clf, entity_spans_pool = self._classify_entities(encodings, h, entity_masks, size_embeddings)
        entity_clf, subtype_clf, entity_spans_pool = self._classify_entities( \
                                            h = h,
                                            entity_masks = entity_masks,
                                            entity_masks_adj = entity_masks_adj,
                                            size_embeddings = size_embeddings,
                                            entity_ctx = entity_ctx)



        # ignore entity candidates that do not constitute an actual entity for relations (based on classifier)
        relations, rel_masks, rel_sample_masks = self._filter_spans(entity_clf, entity_spans,
                                                                    entity_sample_masks, ctx_size)

        rel_sample_masks = rel_sample_masks.float().unsqueeze(-1)
        h_large = h.unsqueeze(1).repeat(1, max(min(relations.shape[1], self._max_pairs), 1), 1, 1)
        rel_clf = torch.zeros([batch_size, relations.shape[1], self._relation_types]).to(
            h.device)
            # self.rel_classifier.weight.device)

        # obtain relation logits
        # chunk processing to reduce memory usage
        for i in range(0, relations.shape[1], self._max_pairs):
            # classify relation candidates
            chunk_rel_logits = self._classify_relations(entity_spans_pool, size_embeddings,
                                                        relations, rel_masks, h_large, i)
            # apply sigmoid
            chunk_rel_clf = torch.sigmoid(chunk_rel_logits)
            rel_clf[:, i:i + self._max_pairs, :] = chunk_rel_clf

        rel_clf = rel_clf * rel_sample_masks  # mask

        # apply softmax
        entity_clf = torch.softmax(entity_clf, dim=2)



        # return entity_clf, subtype_clf, rel_clf, relations, sent_clf, word_piece_clf
        return entity_clf, subtype_clf, rel_clf, relations, sent_clf

    #def _classify_entities(self, encodings, h, entity_masks, size_embeddings):
    def _classify_entities(self, h, entity_masks, entity_masks_adj, size_embeddings, entity_ctx):
        # max pool entity candidate spans
        # entity_masks  (batch_size, pos_entities + negative examples, max_length)
        #               (2,          103,                              25)
        # m             (batch_size, pos_entities + negative examples, max_length, 1)
        # h             (batch_size, max_length, embed_dim)
        #               (2, 25, 768)
        m = (entity_masks.unsqueeze(-1) == 0).float() * (-1e30)

        # entity_spans_pool  (batch_size, pos_entities + negative examples, max_length, embed_dim)
        #                    (2,          103,                              25, 768)
        entity_spans_pool =     m + h.unsqueeze(1).repeat(1, entity_masks.shape[1],     1, 1)
        entity_spans_pool_adj = m + h.unsqueeze(1).repeat(1, entity_masks_adj.shape[1], 1, 1)

        # entity_spans_pool  (batch_size, pos_entities + negative examples, embed_dim)
        #                    (2,          103,                              768)
        entity_spans_pool =     entity_spans_pool.max(dim=2)[0]
        entity_spans_pool_adj = entity_spans_pool_adj.max(dim=2)[0]

        # get cls token as candidate context representation
        #entity_ctx = get_token(h, encodings, self._cls_token)

        # create candidate representations including context, max pooled span and size embedding
        entity_ctx = entity_ctx.unsqueeze(1).repeat(1, entity_spans_pool.shape[1], 1)

        entity_repr = torch.cat([entity_ctx, entity_spans_pool, size_embeddings], dim=2)
        if self.include_adjacent:
            entity_repr = torch.cat([entity_repr, entity_spans_pool_adj], dim=2)


        entity_repr = self.dropout(entity_repr)

        # classify entity candidates
        entity_clf = self.entity_classifier(entity_repr)


        subtype_repr = entity_repr
        # if self.subtype_classification in [NO_SUBTYPE, NO_CONCAT, LABEL_BIAS]:
        if self.subtype_classification in [NO_SUBTYPE, NO_CONCAT]:
            pass
        elif self.subtype_classification == CONCAT_LOGITS:
            subtype_repr = torch.cat([subtype_repr, entity_clf], dim=2)
        elif self.subtype_classification == CONCAT_PROBS:
            subtype_repr = F.softmax(entity_clf, dim=-1)
            subtype_repr = torch.cat([subtype_repr, entity_prob], dim=2)
        else:
            raise ValueError(f"Invalid subtype classification: {self.subtype_classification}")


        subtype_clf = OrderedDict()
        for layer_name, subtype_classifier in self.subtype_classifiers.items():
            subtype_clf[layer_name] = subtype_classifier(subtype_repr)

        # if self.subtype_classification == LABEL_BIAS:
            # subtype_clf += self.subtype_bias(entity_clf)

        return entity_clf, subtype_clf, entity_spans_pool


    def _classify_word_pieces(self, h, include):

        if include:
            h = self.dropout(h)
            word_piece_clf = self.word_piece_classifier(h)
        else:
            word_piece_clf = None

        return word_piece_clf


    def _classify_relations(self, entity_spans, size_embeddings, relations, rel_masks, h, chunk_start):
        batch_size = relations.shape[0]

        # create chunks if necessary
        if relations.shape[1] > self._max_pairs:
            relations = relations[:, chunk_start:chunk_start + self._max_pairs]
            rel_masks = rel_masks[:, chunk_start:chunk_start + self._max_pairs]
            h = h[:, :relations.shape[1], :]

        # get pairs of entity candidate representations
        entity_pairs = util.batch_index(entity_spans, relations)
        entity_pairs = entity_pairs.view(batch_size, entity_pairs.shape[1], -1)

        # get corresponding size embeddings
        size_pair_embeddings = util.batch_index(size_embeddings, relations)
        size_pair_embeddings = size_pair_embeddings.view(batch_size, size_pair_embeddings.shape[1], -1)

        # relation context (context between entity candidate pair)
        # mask non entity candidate tokens
        m = ((rel_masks == 0).float() * (-1e30)).unsqueeze(-1)
        rel_ctx = m + h
        # max pooling
        rel_ctx = rel_ctx.max(dim=2)[0]
        # set the context vector of neighboring or adjacent entity candidates to zero
        rel_ctx[rel_masks.to(torch.uint8).any(-1) == 0] = 0

        # create relation candidate representations including context, max pooled entity candidate pairs
        # and corresponding size embeddings
        rel_repr = torch.cat([rel_ctx, entity_pairs, size_pair_embeddings], dim=2)
        rel_repr = self.dropout(rel_repr)

        # classify relation candidates
        chunk_rel_logits = self.rel_classifier(rel_repr)
        return chunk_rel_logits

    #def _classify_sentences(self, encodings, h):
    def _classify_sentences(self, cls_embedding):

        # get cls token as candidate context representation
        #ctx = get_token(h, encodings, self._cls_token)

        # classify entity candidates
        #clf = self.sent_classifier(ctx)
        clf = self.sent_classifier(cls_embedding)

        return clf


    def _filter_spans(self, entity_clf, entity_spans, entity_sample_masks, ctx_size):
        batch_size = entity_clf.shape[0]
        entity_logits_max = entity_clf.argmax(dim=-1) * entity_sample_masks.long()  # get entity type (including none)
        batch_relations = []
        batch_rel_masks = []
        batch_rel_sample_masks = []

        for i in range(batch_size):
            rels = []
            rel_masks = []
            sample_masks = []

            # get spans classified as entities
            non_zero_indices = (entity_logits_max[i] != 0).nonzero().view(-1)
            non_zero_spans = entity_spans[i][non_zero_indices].tolist()
            non_zero_indices = non_zero_indices.tolist()

            # create relations and masks
            for i1, s1 in zip(non_zero_indices, non_zero_spans):
                for i2, s2 in zip(non_zero_indices, non_zero_spans):
                    if i1 != i2:
                        rels.append((i1, i2))
                        rel_masks.append(sampling.create_rel_mask(s1, s2, ctx_size))
                        sample_masks.append(1)

            if not rels:
                # case: no more than two spans classified as entities
                batch_relations.append(torch.tensor([[0, 0]], dtype=torch.long))
                batch_rel_masks.append(torch.tensor([[0] * ctx_size], dtype=torch.bool))
                batch_rel_sample_masks.append(torch.tensor([0], dtype=torch.bool))
            else:
                # case: more than two spans classified as entities
                batch_relations.append(torch.tensor(rels, dtype=torch.long))
                batch_rel_masks.append(torch.stack(rel_masks))
                batch_rel_sample_masks.append(torch.tensor(sample_masks, dtype=torch.bool))

        # stack
        #device = self.rel_classifier.weight.device
        device = entity_clf.device

        batch_relations = util.padded_stack(batch_relations).to(device)
        batch_rel_masks = util.padded_stack(batch_rel_masks).to(device)
        batch_rel_sample_masks = util.padded_stack(batch_rel_sample_masks).to(device)

        return batch_relations, batch_rel_masks, batch_rel_sample_masks

    def forward(self, *args, inference=False, **kwargs):
        if not inference:
            return self._forward_train(*args, **kwargs)
        else:
            return self._forward_inference(*args, **kwargs)


# Model access

_MODELS = {
    'spert': SpERT,
}


def get_model(name):
    return _MODELS[name]
