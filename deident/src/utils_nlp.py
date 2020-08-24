'''
Miscellaneous utility functions for natural language processing
'''
import codecs
import re
import src.utils as utils
import os
import numpy as np

def load_tokens_from_pretrained_token_embeddings(parameters):
    file_input = codecs.open(parameters['token_pretrained_embedding_filepath'], 'r', 'UTF-8')
    count = -1
    tokens = set()
    number_of_loaded_word_vectors = 0
    for cur_line in file_input:
        count += 1
        cur_line = cur_line.strip()
        cur_line = cur_line.split(' ')
        if len(cur_line)==0:continue
        token=cur_line[0]
        tokens.add(token)
        number_of_loaded_word_vectors += 1
    file_input.close()
    return tokens

def load_pretrained_token_embeddings(parameters):
    file_input = codecs.open(parameters['token_pretrained_embedding_filepath'], 'r', 'UTF-8')
    count = -1
    token_to_vector = {}
    for cur_line in file_input:
        count += 1
        #if count > 1000:break
        cur_line = cur_line.strip()
        cur_line = cur_line.split(' ')
        if len(cur_line)==0:continue
        token = cur_line[0]
        vector = np.array([float(x) for x in cur_line[1:]])
        token_to_vector[token] = vector
    file_input.close()
    return token_to_vector

def is_token_in_pretrained_embeddings(token, all_pretrained_tokens, parameters):
    return token in all_pretrained_tokens or \
        parameters['check_for_lowercase'] and token.lower() in all_pretrained_tokens or \
        parameters['check_for_digits_replaced_with_zeros'] and re.sub('\d', '0', token) in all_pretrained_tokens or \
        parameters['check_for_lowercase'] and parameters['check_for_digits_replaced_with_zeros'] and re.sub('\d', '0', token.lower()) in all_pretrained_tokens
        
def replace_unicode_whitespaces_with_ascii_whitespace(string):
    return ' '.join(string.split())

def end_current_entity(previous_label_without_bio, current_entity_length, new_labels, i):
    '''
    Helper function for bio_to_bioes
    '''
    if current_entity_length == 0:
        return
    if current_entity_length == 1:
        new_labels[i - 1] = 'S-' + previous_label_without_bio
    else: #elif current_entity_length > 1
        new_labels[i - 1] = 'E-' + previous_label_without_bio 


def remove_bio_from_label_name(label_name):
    if label_name[:2] in ['B-', 'I-', 'E-', 'S-']:
        new_label_name = label_name[2:]
    else:
        assert(label_name == 'O')
        new_label_name = label_name
    return new_label_name


def bio_to_bioes(labels):
    previous_label_without_bio = 'O'
    current_entity_length = 0
    new_labels = labels.copy()
    for i, label in enumerate(labels):
        label_without_bio = remove_bio_from_label_name(label)
        # end the entity
        if current_entity_length > 0 and (label[:2] in ['B-', 'O'] or label[:2] == 'I-' and previous_label_without_bio != label_without_bio):
            end_current_entity(previous_label_without_bio, current_entity_length, new_labels, i)
            current_entity_length = 0
        if label[:2] == 'B-':
            current_entity_length = 1
        elif label[:2] == 'I-':
            if current_entity_length == 0:
                new_labels[i] = 'B-' + label_without_bio
            current_entity_length += 1
        previous_label_without_bio = label_without_bio    
    end_current_entity(previous_label_without_bio, current_entity_length, new_labels, i + 1)
    return new_labels


def bioes_to_bio(labels):
    previous_label_without_bio = 'O'
    new_labels = labels.copy()
    for i, label in enumerate(labels):
        label_without_bio = remove_bio_from_label_name(label)
        if label[:2] in ['I-', 'E-']:
            if previous_label_without_bio == label_without_bio:
                new_labels[i] = 'I-' + label_without_bio
            else:
                new_labels[i] = 'B-' + label_without_bio
        elif label[:2] in ['S-']:
            new_labels[i] = 'B-' + label_without_bio
        previous_label_without_bio = label_without_bio
    return new_labels
                

def check_bio_bioes_compatibility(labels_bio, labels_bioes):
    if labels_bioes == []:
        return True
    new_labels_bio = bioes_to_bio(labels_bioes)
    flag = True
    if new_labels_bio != labels_bio:
        print("Not valid.")
        flag = False 
    del labels_bio[:]
    del labels_bioes[:]
    return flag


def convert_conll_from_bio_to_bioes(text):
    output = ''
    labels = []
    split_lines = []
    for line in text.splitlines():
        split_line = line.strip().split(' ')
        # New sentence
        if len(split_line) == 0 or len(split_line[0]) == 0 or '-DOCSTART-' in split_line[0]:
            output = output_conll_lines_with_bioes(split_lines, labels, output)
            output += line
            continue
        label = split_line[-1]    
        labels.append(label)
        split_lines.append(split_line)
    output = output_conll_lines_with_bioes(split_lines, labels, output)
    
    return output
    
def output_conll_lines_with_bioes(split_lines, labels, output):
    '''
    Helper function for convert_conll_from_bio_to_bioes
    '''
    if labels == []:
        return
    new_labels = bio_to_bioes(labels)
    assert(len(new_labels) == len(split_lines))
    for split_line, new_label in zip(split_lines, new_labels):
        output += ' '.join(split_line + [new_label]) + '\n'
    del labels[:]
    del split_lines[:]
    return output