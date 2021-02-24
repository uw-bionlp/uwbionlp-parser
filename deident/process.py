import os

from nn.neuroner import NeuroNER
from proto.python.uwbionlp_pb2 import DeidentificationOutput, PredictionEventArgument

class DocumentProcessor():

    def __init__(self):
        self.nn = NeuroNER(params())

    def predict(self, text):
        try:
            predictions = self.nn.predict(text)
        except Exception as ex:
            return DeidentificationOutput()

        # Return Protobuf Result object.
        result = DeidentificationOutput()
        deident_text = text
        offset = 0
        for pred in predictions:
            entity = PredictionEventArgument()
            entity.char_start_idx = pred['start']
            entity.char_end_idx = pred['end']
            entity.label = pred['label']
            entity.text = text[pred['start']:pred['end']]
            entity.type = 'PHI'
            result.named_entities.append(entity)
            deident_text = deident_text[:pred['start']+offset] + f'<{pred["label"]}/>' + deident_text[pred['end']+offset:]
            offset = len(deident_text)-len(text)
        result.deident_text = deident_text

        return result

def params():
    model_dir = 'trained_models'
    model = [ d for d in os.listdir(model_dir) if os.path.isdir(os.path.join(model_dir, d)) ][0]
    parameters = {'pretrained_model_folder': os.path.join(model_dir, model),
                  'dataset_text_folder':'./data/test_data',
                  'character_embedding_dimension':25,
                  'character_lstm_hidden_state_dimension':25,
                  'check_for_digits_replaced_with_zeros':True,
                  'check_for_lowercase':True,
                  'debug':False,
                  'dropout_rate':0.5,
                  'experiment_name':'experiment',
                  'freeze_token_embeddings':False,
                  'gradient_clipping_value':5.0,
                  'learning_rate':0.005,
                  'load_all_pretrained_token_embeddings':False,
                  'load_only_pretrained_token_embeddings':False,
                  'main_evaluation_mode':'conll',
                  'maximum_number_of_epochs':100,
                  'number_of_cpu_threads':4,
                  'number_of_gpus':0,
                  'optimizer':'sgd',
                  'output_folder':'../output',
                  'patience':10,
                  'plot_format':'pdf',
                  'reload_character_embeddings':True,
                  'reload_character_lstm':True,
                  'reload_crf':True,
                  'reload_feedforward':True,
                  'reload_token_embeddings':True,
                  'reload_token_lstm':True,
                  'remap_unknown_tokens_to_unk':True,
                  'spacylanguage':'en',
                  'tagging_format':'bioes',
                  'token_embedding_dimension':100,
                  'token_lstm_hidden_state_dimension':100,
                  'token_pretrained_embedding_filepath':'./data/word_vectors/glove.6B.100d.txt',
                  'tokenizer':'spacy',
                  'train_model':False,
                  'use_character_lstm':True,
                  'use_crf':True,
                  'use_pretrained_model':True,
                  'verbose':False}
    return parameters