import tensorflow as tf
import re
import time
import os
import pickle
import nn.utils_tf as utils_tf
import nn.utils_nlp as utils_nlp


def bidirectional_LSTM(input, hidden_state_dimension, initializer, sequence_length=None, output_sequence=True):

    with tf.variable_scope("bidirectional_LSTM"):
        if sequence_length == None:
            batch_size = 1
            sequence_length = tf.shape(input)[1]
            sequence_length = tf.expand_dims(sequence_length, axis=0, name='sequence_length')
        else:
            batch_size = tf.shape(sequence_length)[0]

        lstm_cell = {}
        initial_state = {}
        for direction in ["forward", "backward"]:
            with tf.variable_scope(direction):
                # LSTM cell
                lstm_cell[direction] = tf.contrib.rnn.CoupledInputForgetGateLSTMCell(hidden_state_dimension, forget_bias=1.0, initializer=initializer, state_is_tuple=True)
                # initial state: http://stackoverflow.com/questions/38441589/tensorflow-rnn-initial-state
                initial_cell_state = tf.get_variable("initial_cell_state", shape=[1, hidden_state_dimension], dtype=tf.float32, initializer=initializer)
                initial_output_state = tf.get_variable("initial_output_state", shape=[1, hidden_state_dimension], dtype=tf.float32, initializer=initializer)
                c_states = tf.tile(initial_cell_state, tf.stack([batch_size, 1]))
                h_states = tf.tile(initial_output_state, tf.stack([batch_size, 1]))
                initial_state[direction] = tf.contrib.rnn.LSTMStateTuple(c_states, h_states)

        # sequence_length must be provided for tf.nn.bidirectional_dynamic_rnn due to internal bug
        outputs, final_states = tf.nn.bidirectional_dynamic_rnn(lstm_cell["forward"],
                                                                    lstm_cell["backward"],
                                                                    input,
                                                                    dtype=tf.float32,
                                                                    sequence_length=sequence_length,
                                                                    initial_state_fw=initial_state["forward"],
                                                                    initial_state_bw=initial_state["backward"])
        # for token embedding
        if output_sequence == True:
            outputs_forward, outputs_backward = outputs
            output = tf.concat([outputs_forward, outputs_backward], axis=2, name='output_sequence')
        # for character embedding
        else:
            final_states_forward, final_states_backward = final_states
            output = tf.concat([final_states_forward[1], final_states_backward[1]], axis=1, name='output')

    return output
    

class EntityLSTM(object):

    """
    An LSTM architecture for named entity recognition.
    Uses a character embedding layer followed by an LSTM to generate vector representation from characters for each token.
    Then the character vector is concatenated with token embedding vector, which is input to another LSTM  followed by a CRF layer.
    """
    def __init__(self, dataset, parameters, initializer):

        # Placeholders for input, output and dropout
        self.input_token_indices = tf.placeholder(tf.int32, [None], name="input_token_indices")
        self.input_label_indices_vector = tf.placeholder(tf.float32, [None, dataset.number_of_classes], name="input_label_indices_vector")
        self.input_label_indices_flat = tf.placeholder(tf.int32, [None], name="input_label_indices_flat")
        self.input_token_character_indices = tf.placeholder(tf.int32, [None, None], name="input_token_indices")
        self.input_token_lengths = tf.placeholder(tf.int32, [None], name="input_token_lengths")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        if parameters['use_character_lstm']:
            # Character-level LSTM
            # Idea: reshape so that we have a tensor [number_of_token, max_token_length, token_embeddings_size], which we pass to the LSTM

            # Character embedding layer
            with tf.variable_scope("character_embedding"):
                self.character_embedding_weights = tf.get_variable(
                    "character_embedding_weights",
                    shape=[dataset.alphabet_size, parameters['character_embedding_dimension']],
                    initializer=initializer)
                self.embedded_characters = tf.nn.embedding_lookup(self.character_embedding_weights, self.input_token_character_indices, name='embedded_characters')
                embedded_characters = self.embedded_characters

            # Character LSTM layer
            with tf.variable_scope('character_lstm') as vs:
                self.character_lstm_output = bidirectional_LSTM(embedded_characters, parameters['character_lstm_hidden_state_dimension'], initializer,
                                                        sequence_length=self.input_token_lengths, output_sequence=False)
                self.character_lstm_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)
                character_lstm_output = self.character_lstm_output


        # Token embedding layer
        with tf.variable_scope("token_embedding"):
            self.token_embedding_weights = tf.get_variable(
                "token_embedding_weights",
                shape=[dataset.vocabulary_size, parameters['token_embedding_dimension']],
                initializer=initializer,
                trainable=not parameters['freeze_token_embeddings'])
            embedded_tokens = tf.nn.embedding_lookup(self.token_embedding_weights, self.input_token_indices)

        # Concatenate character LSTM outputs and token embeddings
        if parameters['use_character_lstm']:
            with tf.variable_scope("concatenate_token_and_character_vectors"):
                token_lstm_input = tf.concat([character_lstm_output, embedded_tokens], axis=1, name='token_lstm_input')
        else:
            token_lstm_input = embedded_tokens

        # Add dropout
        with tf.variable_scope("dropout"):
            token_lstm_input_drop = tf.nn.dropout(token_lstm_input, self.dropout_keep_prob, name='token_lstm_input_drop')
            token_lstm_input_drop_expanded = tf.expand_dims(token_lstm_input_drop, axis=0, name='token_lstm_input_drop_expanded')

        # Token LSTM layer
        with tf.variable_scope('token_lstm') as vs:
            token_lstm_output = bidirectional_LSTM(token_lstm_input_drop_expanded, parameters['token_lstm_hidden_state_dimension'], initializer, output_sequence=True)
            token_lstm_output_squeezed = tf.squeeze(token_lstm_output, axis=0)
            self.token_lstm_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)

        # Needed only if Bidirectional LSTM is used for token level
        with tf.variable_scope("feedforward_after_lstm") as vs:
            W = tf.get_variable(
                "W",
                shape=[2 * parameters['token_lstm_hidden_state_dimension'], parameters['token_lstm_hidden_state_dimension']],
                initializer=initializer)
            b = tf.Variable(tf.constant(0.0, shape=[parameters['token_lstm_hidden_state_dimension']]), name="bias")
            outputs = tf.nn.xw_plus_b(token_lstm_output_squeezed, W, b, name="output_before_tanh")
            outputs = tf.nn.tanh(outputs, name="output_after_tanh")
            self.token_lstm_variables += tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)

        with tf.variable_scope("feedforward_before_crf", reuse=tf.AUTO_REUSE) as vs:
            W = tf.get_variable(
                "W",
                shape=[parameters['token_lstm_hidden_state_dimension'], dataset.number_of_classes],
                initializer=initializer)
            b = tf.Variable(tf.constant(0.0, shape=[dataset.number_of_classes]), name="bias")
            scores = tf.nn.xw_plus_b(outputs, W, b, name="scores")
            self.unary_scores = scores
            self.predictions = tf.argmax(self.unary_scores, 1, name="predictions")
            self.feedforward_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)

        # CRF layer
        if parameters['use_crf']:
            with tf.variable_scope("crf") as vs:
                # Add start and end tokens
                small_score = -1000.0
                large_score = 0.0
                sequence_length = tf.shape(self.unary_scores)[0]
                unary_scores_with_start_and_end = tf.concat([self.unary_scores, tf.tile( tf.constant(small_score, shape=[1, 2]) , [sequence_length, 1])], 1)
                start_unary_scores = [[small_score] * dataset.number_of_classes + [large_score, small_score]]
                end_unary_scores = [[small_score] * dataset.number_of_classes + [small_score, large_score]]
                self.unary_scores = tf.concat([start_unary_scores, unary_scores_with_start_and_end, end_unary_scores], 0)
                start_index = dataset.number_of_classes
                end_index = dataset.number_of_classes + 1
                input_label_indices_flat_with_start_and_end = tf.concat([ tf.constant(start_index, shape=[1]), self.input_label_indices_flat, tf.constant(end_index, shape=[1]) ], 0)

                # Apply CRF layer
                sequence_length = tf.shape(self.unary_scores)[0]
                sequence_lengths = tf.expand_dims(sequence_length, axis=0, name='sequence_lengths')
                unary_scores_expanded = tf.expand_dims(self.unary_scores, axis=0, name='unary_scores_expanded')
                input_label_indices_flat_batch = tf.expand_dims(input_label_indices_flat_with_start_and_end, axis=0, name='input_label_indices_flat_batch')
                self.transition_parameters=tf.get_variable(
                    "transitions",
                    shape=[dataset.number_of_classes+2, dataset.number_of_classes+2],
                    initializer=initializer)
                utils_tf.variable_summaries(self.transition_parameters)
                log_likelihood, _ = tf.contrib.crf.crf_log_likelihood(
                    unary_scores_expanded, input_label_indices_flat_batch, sequence_lengths, transition_params=self.transition_parameters)
                self.loss =  tf.reduce_mean(-log_likelihood, name='cross_entropy_mean_loss')
                self.accuracy = tf.constant(1)
                self.crf_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)

        self.saver = tf.train.Saver(max_to_keep=parameters['maximum_number_of_epochs'])  # defaults to saving all variables

    def load_pretrained_token_embeddings(self, sess, dataset, parameters, token_to_vector=None):
        if parameters['token_pretrained_embedding_filepath'] == '':
            return
        # Load embeddings
        start_time = time.time()
        if token_to_vector == None:
            token_to_vector = utils_nlp.load_pretrained_token_embeddings(parameters)

        initial_weights = sess.run(self.token_embedding_weights.read_value())
        number_of_loaded_word_vectors = 0
        number_of_token_original_case_found = 0
        number_of_token_lowercase_found = 0
        number_of_token_digits_replaced_with_zeros_found = 0
        number_of_token_lowercase_and_digits_replaced_with_zeros_found = 0
        for token in dataset.token_to_index.keys():
            if token in token_to_vector.keys():
                initial_weights[dataset.token_to_index[token]] = token_to_vector[token]
                number_of_token_original_case_found += 1
            elif parameters['check_for_lowercase'] and token.lower() in token_to_vector.keys():
                initial_weights[dataset.token_to_index[token]] = token_to_vector[token.lower()]
                number_of_token_lowercase_found += 1
            elif parameters['check_for_digits_replaced_with_zeros'] and re.sub('\d', '0', token) in token_to_vector.keys():
                initial_weights[dataset.token_to_index[token]] = token_to_vector[re.sub('\d', '0', token)]
                number_of_token_digits_replaced_with_zeros_found += 1
            elif parameters['check_for_lowercase'] and parameters['check_for_digits_replaced_with_zeros'] and re.sub('\d', '0', token.lower()) in token_to_vector.keys():
                initial_weights[dataset.token_to_index[token]] = token_to_vector[re.sub('\d', '0', token.lower())]
                number_of_token_lowercase_and_digits_replaced_with_zeros_found += 1
            else:
                continue
            number_of_loaded_word_vectors += 1
        elapsed_time = time.time() - start_time
        sess.run(self.token_embedding_weights.assign(initial_weights))

    def load_embeddings_from_pretrained_model(self, sess, dataset, pretraining_dataset, pretrained_embedding_weights, embedding_type='token'):
        if embedding_type == 'token':
            embedding_weights = self.token_embedding_weights
            index_to_string = dataset.index_to_token
            pretraining_string_to_index = pretraining_dataset.token_to_index
        elif embedding_type == 'character':
            embedding_weights = self.character_embedding_weights
            index_to_string = dataset.index_to_character
            pretraining_string_to_index = pretraining_dataset.character_to_index
        # Load embeddings
        initial_weights = sess.run(embedding_weights.read_value())

        if embedding_type == 'token':
            initial_weights[dataset.UNK_TOKEN_INDEX] = pretrained_embedding_weights[pretraining_dataset.UNK_TOKEN_INDEX]
        elif embedding_type == 'character':
            initial_weights[dataset.PADDING_CHARACTER_INDEX] = pretrained_embedding_weights[pretraining_dataset.PADDING_CHARACTER_INDEX]

        number_of_loaded_vectors = 1
        for index, string in index_to_string.items():
            if index == dataset.UNK_TOKEN_INDEX:
                continue
            if string in pretraining_string_to_index.keys():
                initial_weights[index] = pretrained_embedding_weights[pretraining_string_to_index[string]]
                number_of_loaded_vectors += 1
        sess.run(embedding_weights.assign(initial_weights))

    def restore_from_pretrained_model(self, pretraining_dataset, parameters, dataset, sess, token_to_vector=None):
        pretrained_model_checkpoint_filepath = os.path.join(parameters['pretrained_model_folder'], 'model.ckpt')
        
        # Assert that the label sets are the same
        # Test set should have the same label set as the pretrained dataset
        assert pretraining_dataset.index_to_label == dataset.index_to_label
    
        # If the token and character mappings are exactly the same
        if pretraining_dataset.index_to_token == dataset.index_to_token and pretraining_dataset.index_to_character == dataset.index_to_character:
            
            # Restore the pretrained model
            self.saver.restore(sess, pretrained_model_checkpoint_filepath) # Works only when the dimensions of tensor variables are matched.
        
        # If the token and character mappings are different between the pretrained model and the current model
        else:
            
            # Resize the token and character embedding weights to match them with the pretrained model (required in order to restore the pretrained model)
            utils_tf.resize_tensor_variable(sess, self.character_embedding_weights, [pretraining_dataset.alphabet_size, parameters['character_embedding_dimension']])
            utils_tf.resize_tensor_variable(sess, self.token_embedding_weights, [pretraining_dataset.vocabulary_size, parameters['token_embedding_dimension']])
        
            # Restore the pretrained model
            self.saver.restore(sess, pretrained_model_checkpoint_filepath) # Works only when the dimensions of tensor variables are matched.
            
            # Get pretrained embeddings
            character_embedding_weights, token_embedding_weights = sess.run([self.character_embedding_weights, self.token_embedding_weights]) 
            
            # Restore the sizes of token and character embedding weights
            utils_tf.resize_tensor_variable(sess, self.character_embedding_weights, [dataset.alphabet_size, parameters['character_embedding_dimension']])
            utils_tf.resize_tensor_variable(sess, self.token_embedding_weights, [dataset.vocabulary_size, parameters['token_embedding_dimension']]) 
            
            # Re-initialize the token and character embedding weights
            sess.run(tf.variables_initializer([self.character_embedding_weights, self.token_embedding_weights]))
            
            # Load embedding weights from pretrained token embeddings first
            self.load_pretrained_token_embeddings(sess, dataset, parameters, token_to_vector=token_to_vector) 
            
            # Load embedding weights from pretrained model
            self.load_embeddings_from_pretrained_model(sess, dataset, pretraining_dataset, token_embedding_weights, embedding_type='token')
            self.load_embeddings_from_pretrained_model(sess, dataset, pretraining_dataset, character_embedding_weights, embedding_type='character') 
        
        # Get transition parameters
        transition_params_trained = sess.run(self.transition_parameters)
        
        if not parameters['reload_character_embeddings']:
            sess.run(tf.variables_initializer([self.character_embedding_weights]))
        if not parameters['reload_character_lstm']:
            sess.run(tf.variables_initializer(self.character_lstm_variables))
        if not parameters['reload_token_embeddings']:
            sess.run(tf.variables_initializer([self.token_embedding_weights]))
        if not parameters['reload_token_lstm']:
            sess.run(tf.variables_initializer(self.token_lstm_variables))
        if not parameters['reload_feedforward']:
            sess.run(tf.variables_initializer(self.feedforward_variables))
        if not parameters['reload_crf']:
            sess.run(tf.variables_initializer(self.crf_variables))
    
        return transition_params_trained