import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'nn'))
from nn.neuroner import NeuroNER

def run():
    nn = NeuroNER(params())
    ex1 = nn.predict(""" Mr Garret is a 40 year old man born on May 4th 1942 and his phone number is 204-412-5932 """)
    print(ex1)
    ex2 = nn.predict("""Dr Shobbins has is MRN23573 """)
    print(ex2)

def params():
    parameters = {'pretrained_model_folder':'./trained_models/deident',
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

if __name__ == '__main__':
    run()