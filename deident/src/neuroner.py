import os
import sys
import matplotlib
matplotlib.use('Agg')
import pickle
import src.train as train
import src.dataset as ds
from src.entity_lstm import EntityLSTM
from src.conll_to_objects import conll_to_objects
from src.brat_to_conll import brat_to_conll 
from src.utils_nlp import convert_conll_from_bio_to_bioes, load_pretrained_token_embeddings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import traceback


class NeuroNER(object):
    def __init__(self, parameters):
        self.session_conf = tf.ConfigProto(
            intra_op_parallelism_threads=parameters['number_of_cpu_threads'],
            inter_op_parallelism_threads=parameters['number_of_cpu_threads'],
            device_count={'CPU': 1, 'GPU': parameters['number_of_gpus']},
            allow_soft_placement=True, 
            log_device_placement=False
        )
        self.parameters = parameters
        self.model_loaded = False

    def load_model(self):
        self.pretraining_dataset = pickle.load(open(os.path.join(self.parameters['pretrained_model_folder'], 'dataset.pickle'), 'rb'))
        self.all_tokens_in_pretraining_dataset = self.pretraining_dataset.index_to_token.values()
        self.all_characters_in_pretraining_dataset = self.pretraining_dataset.index_to_character.values()
        self.token_to_vector = load_pretrained_token_embeddings(self.parameters)
        self.model_loaded = True

    def predict(self, text):
        tf.reset_default_graph()
        if not self.model_loaded:
            self.load_model()

        sess = tf.Session(config=self.session_conf)
        with sess.as_default():
            sess.run(tf.global_variables_initializer())
            conll = brat_to_conll(text)
            bioes = convert_conll_from_bio_to_bioes(conll)
            dataset = ds.Dataset(self.token_to_vector)
            dataset.load_dataset(bioes, self.parameters, self.pretraining_dataset, self.all_tokens_in_pretraining_dataset, self.all_characters_in_pretraining_dataset)
            model = EntityLSTM(dataset, self.parameters)
            transition_params_trained = model.restore_from_pretrained_model(self.pretraining_dataset, self.parameters, dataset, sess, token_to_vector=self.token_to_vector)
            try:
                _, _, output = train.prediction_step(sess, bioes, dataset, model, transition_params_trained, self.parameters)
                entities = conll_to_objects(output)
                return entities
            except Exception as ex:
                traceback.print_stack()
                return []
        
    

