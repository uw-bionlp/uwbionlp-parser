import os
import tensorflow as tf
from nn.utils_nlp import bioes_to_bio


def prediction_step(sess, bioes, dataset, model, transition_params_trained, parameters):
    output = ''
    dataset_type = 'deploy'
    all_predictions = []
    all_y_true = []

    for i in range(len(dataset.token_indices[dataset_type])):
        feed_dict = {
          model.input_token_indices: dataset.token_indices[dataset_type][i],
          model.input_token_character_indices: dataset.character_indices_padded[dataset_type][i],
          model.input_token_lengths: dataset.token_lengths[dataset_type][i],
          model.input_label_indices_vector: dataset.label_vector_indices[dataset_type][i],
          model.dropout_keep_prob: 1.
        }
        unary_scores, predictions = sess.run([model.unary_scores, model.predictions], feed_dict)
        if parameters['use_crf']:
            predictions, _ = tf.contrib.crf.viterbi_decode(unary_scores, transition_params_trained)
            predictions = predictions[1:-1]
        else:
            predictions = predictions.tolist()

        assert(len(predictions) == len(dataset.tokens[dataset_type][i]))
        prediction_labels = [dataset.index_to_label[prediction] for prediction in predictions]
        gold_labels = dataset.labels[dataset_type][i]

        if parameters['tagging_format'] == 'bioes':
            prediction_labels = bioes_to_bio(prediction_labels)
            gold_labels = bioes_to_bio(gold_labels)

        lines, j = bioes.splitlines(), 0
        for prediction, token, gold_label in zip(prediction_labels, dataset.tokens[dataset_type][i], gold_labels):
            while True:
                line = lines[j]
                j += 1
                split_line = line.strip().split(' ')
                if '-DOCSTART-' in split_line[0] or len(split_line) == 0 or len(split_line[0]) == 0:
                    continue
                else:
                    token_original = split_line[0]
                    if parameters['tagging_format'] == 'bioes':
                        split_line.pop()
                    gold_label_original = split_line[-1]
                    assert(token == token_original and gold_label == gold_label_original) 
                    break            
            split_line.append(prediction)
            output += ' '.join(split_line) + '\n'

        all_predictions.extend(predictions)
        all_y_true.extend(dataset.label_indices[dataset_type][i])    

    return all_predictions, all_y_true, output