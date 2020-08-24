import collections
import os
import random
import sklearn.preprocessing
import src.utils as utils
import src.utils_nlp as utils_nlp


class Dataset(object):
    """A class for handling data sets."""

    def __init__(self, token_to_vector):
        self.name = ''
        self.verbose = False
        self.debug = False
        self.token_to_vector = token_to_vector

    def _parse_dataset(self, text):
        token_count = collections.defaultdict(lambda: 0)
        label_count = collections.defaultdict(lambda: 0)
        character_count = collections.defaultdict(lambda: 0)

        line_count = -1
        tokens = []
        labels = []
        new_token_sequence = []
        new_label_sequence = []
        if text:
            for line in text.splitlines():
                line_count += 1
                line = line.strip().split(' ')
                if len(line) == 0 or len(line[0]) == 0 or '-DOCSTART-' in line[0]:
                    if len(new_token_sequence) > 0:
                        labels.append(new_label_sequence)
                        tokens.append(new_token_sequence)
                        new_token_sequence = []
                        new_label_sequence = []
                    continue
                token = str(line[0])
                label = str(line[-1])
                token_count[token] += 1
                label_count[label] += 1

                new_token_sequence.append(token)
                new_label_sequence.append(label)

                for character in token:
                    character_count[character] += 1

            if len(new_token_sequence) > 0:
                labels.append(new_label_sequence)
                tokens.append(new_token_sequence)
            
        return labels, tokens, token_count, label_count, character_count

    def _convert_to_indices(self, dataset_types):
        tokens = self.tokens
        labels = self.labels
        token_to_index = self.token_to_index
        character_to_index = self.character_to_index
        label_to_index = self.label_to_index
        index_to_label = self.index_to_label
        
        # Map tokens and labels to their indices
        token_indices = {}
        label_indices = {}
        characters = {}
        token_lengths = {}
        character_indices = {}
        character_indices_padded = {}
        for dataset_type in dataset_types:
            token_indices[dataset_type] = []
            characters[dataset_type] = []
            character_indices[dataset_type] = []
            token_lengths[dataset_type] = []
            character_indices_padded[dataset_type] = []
            for token_sequence in tokens[dataset_type]:
                token_indices[dataset_type].append([token_to_index.get(token, self.UNK_TOKEN_INDEX) for token in token_sequence])
                characters[dataset_type].append([list(token) for token in token_sequence])
                character_indices[dataset_type].append([[character_to_index.get(character, random.randint(1, max(self.index_to_character.keys()))) for character in token] for token in token_sequence])
                token_lengths[dataset_type].append([len(token) for token in token_sequence])
                longest_token_length_in_sequence = max(token_lengths[dataset_type][-1])
                character_indices_padded[dataset_type].append([utils.pad_list(temp_token_indices, longest_token_length_in_sequence, self.PADDING_CHARACTER_INDEX) for temp_token_indices in character_indices[dataset_type][-1]])
            
            label_indices[dataset_type] = []
            for label_sequence in labels[dataset_type]:
                label_indices[dataset_type].append([label_to_index[label] for label in label_sequence])

        # [Numpy 1-hot array](http://stackoverflow.com/a/42263603/395857)
        label_binarizer = sklearn.preprocessing.LabelBinarizer()
        label_binarizer.fit(range(max(index_to_label.keys()) + 1))
        label_vector_indices = {}
        for dataset_type in dataset_types:
            label_vector_indices[dataset_type] = []
            for label_indices_sequence in label_indices[dataset_type]:
                label_vector_indices[dataset_type].append(label_binarizer.transform(label_indices_sequence))
                
        return token_indices, label_indices, character_indices_padded, character_indices, token_lengths, characters, label_vector_indices


    def load_dataset(self, text, parameters, pretraining_dataset, all_tokens_in_pretraining_dataset, all_characters_in_pretraining_dataset):
        '''
        dataset_filepaths : dictionary with keys 'train', 'valid', 'test', 'deploy'
        '''
        token_to_vector = self.token_to_vector
        remap_to_unk_count_threshold = 1
        self.UNK_TOKEN_INDEX = 0
        self.PADDING_CHARACTER_INDEX = 0
        self.tokens_mapped_to_unk = []
        self.UNK = 'UNK'
        self.unique_labels = []
        labels = {}
        tokens = {}
        label_count = {}
        token_count = {}
        character_count = {}
        for dataset_type in ['test','valid','deploy','train']:
            txt = text if dataset_type == 'deploy' else None
            labels[dataset_type], tokens[dataset_type], token_count[dataset_type], label_count[dataset_type], character_count[dataset_type] \
                = self._parse_dataset(txt)

        token_count['all'] = {}
        for token in list(token_count['train'].keys()) + list(token_count['valid'].keys()) + list(token_count['test'].keys()) + list(token_count['deploy'].keys()):
            token_count['all'][token] = token_count['train'][token] + token_count['valid'][token] + token_count['test'][token] + token_count['deploy'][token]
        
        if parameters['load_all_pretrained_token_embeddings']:
            for token in token_to_vector:
                if token not in token_count['all']:
                    token_count['all'][token] = -1
                    token_count['train'][token] = -1
            for token in all_tokens_in_pretraining_dataset:
                if token not in token_count['all']:
                    token_count['all'][token] = -1
                    token_count['train'][token] = -1

        character_count['all'] = {}
        for character in list(character_count['train'].keys()) + list(character_count['valid'].keys()) + list(character_count['test'].keys()) + list(character_count['deploy'].keys()):
            character_count['all'][character] = character_count['train'][character] + character_count['valid'][character] + character_count['test'][character] + character_count['deploy'][character]

        for character in all_characters_in_pretraining_dataset:
            if character not in character_count['all']:
                character_count['all'][character] = -1
                character_count['train'][character] = -1

        label_count['all'] = {}
        for character in list(label_count['train'].keys()) + list(label_count['valid'].keys()) + list(label_count['test'].keys()) + list(label_count['deploy'].keys()):
            label_count['all'][character] = label_count['train'][character] + label_count['valid'][character] + label_count['test'][character] + label_count['deploy'][character]

        token_count['all'] = utils.order_dictionary(token_count['all'], 'value_key', reverse = True)
        label_count['all'] = utils.order_dictionary(label_count['all'], 'key', reverse = False)
        character_count['all'] = utils.order_dictionary(character_count['all'], 'value', reverse = True)

        token_to_index = {}
        token_to_index[self.UNK] = self.UNK_TOKEN_INDEX
        iteration_number = 0
        number_of_unknown_tokens = 0
        for token, count in token_count['all'].items():
            if iteration_number == self.UNK_TOKEN_INDEX: iteration_number += 1

            if parameters['remap_unknown_tokens_to_unk'] == 1 and \
                (token_count['train'][token] == 0 or \
                parameters['load_only_pretrained_token_embeddings']) and \
                not utils_nlp.is_token_in_pretrained_embeddings(token, token_to_vector, parameters) and \
                token not in all_tokens_in_pretraining_dataset:
                token_to_index[token] =  self.UNK_TOKEN_INDEX
                number_of_unknown_tokens += 1
                self.tokens_mapped_to_unk.append(token)
            else:
                token_to_index[token] = iteration_number
                iteration_number += 1

        infrequent_token_indices = []
        for token, count in token_count['train'].items():
            if 0 < count <= remap_to_unk_count_threshold:
                infrequent_token_indices.append(token_to_index[token])

        # Ensure that both B- and I- versions exist for each label
        labels_without_bio = set()
        for label in label_count['all'].keys():
            new_label = utils_nlp.remove_bio_from_label_name(label)
            labels_without_bio.add(new_label)
        for label in labels_without_bio:
            if label == 'O':
                continue
            if parameters['tagging_format'] == 'bioes':
                prefixes = ['B-', 'I-', 'E-', 'S-']
            else:
                prefixes = ['B-', 'I-']
            for prefix in prefixes:
                l = prefix + label
                if l not in label_count['all']:
                    label_count['all'][l] = 0
        label_count['all'] = utils.order_dictionary(label_count['all'], 'key', reverse = False)

        self.unique_labels = sorted(list(pretraining_dataset.label_to_index.keys()))
        label_to_index = pretraining_dataset.label_to_index.copy()

        character_to_index = {}
        iteration_number = 0
        for character, count in character_count['all'].items():
            if iteration_number == self.PADDING_CHARACTER_INDEX: iteration_number += 1
            character_to_index[character] = iteration_number
            iteration_number += 1

        token_to_index = utils.order_dictionary(token_to_index, 'value', reverse = False)
        index_to_token = utils.reverse_dictionary(token_to_index)
        if parameters['remap_unknown_tokens_to_unk'] == 1: index_to_token[self.UNK_TOKEN_INDEX] = self.UNK

        label_to_index = utils.order_dictionary(label_to_index, 'value', reverse = False)
        index_to_label = utils.reverse_dictionary(label_to_index)

        character_to_index = utils.order_dictionary(character_to_index, 'value', reverse = False)
        index_to_character = utils.reverse_dictionary(character_to_index)

        self.token_to_index = token_to_index
        self.index_to_token = index_to_token
        self.index_to_character = index_to_character
        self.character_to_index = character_to_index
        self.index_to_label = index_to_label
        self.label_to_index = label_to_index
        self.tokens = tokens
        self.labels = labels

        token_indices, label_indices, character_indices_padded, character_indices, token_lengths, characters, label_vector_indices = self._convert_to_indices([ 'deploy' ])
        
        self.token_indices = token_indices
        self.label_indices = label_indices
        self.character_indices_padded = character_indices_padded
        self.character_indices = character_indices
        self.token_lengths = token_lengths
        self.characters = characters
        self.label_vector_indices = label_vector_indices

        self.number_of_classes = max(self.index_to_label.keys()) + 1
        self.vocabulary_size = max(self.index_to_token.keys()) + 1
        self.alphabet_size = max(self.index_to_character.keys()) + 1

        # unique_labels_of_interest is used to compute F1-scores.
        self.unique_labels_of_interest = list(self.unique_labels)
        self.unique_labels_of_interest.remove('O')

        self.unique_label_indices_of_interest = []
        for lab in self.unique_labels_of_interest:
            self.unique_label_indices_of_interest.append(label_to_index[lab])

        self.infrequent_token_indices = infrequent_token_indices
