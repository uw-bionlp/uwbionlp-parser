# -*- coding: utf-8 -*-
import os
import spacy
import src.utils_nlp
spacy_nlp = spacy.load('en')

def get_start_and_end_offset_of_token_from_spacy(token):
    start = token.idx
    end = start + len(token)
    return start, end

def get_sentences_and_tokens_from_spacy(text, spacy_nlp):
    document = spacy_nlp(text)
    # sentences
    sentences = []
    for span in document.sents:
        sentence = [document[i] for i in range(span.start, span.end)]
        sentence_tokens = []
        for token in sentence:
            token_dict = {}
            token_dict['start'], token_dict['end'] = get_start_and_end_offset_of_token_from_spacy(token)
            token_dict['text'] = text[token_dict['start']:token_dict['end']]
            if token_dict['text'].strip() in ['\n', '\t', ' ', '']:
                continue
            # Make sure that the token text does not contain any space
            if len(token_dict['text'].split(' ')) != 1:
                print("WARNING: the text of the token contains space character, replaced with hyphen\n\t{0}\n\t{1}".format(token_dict['text'], 
                                                                                                                           token_dict['text'].replace(' ', '-')))
                token_dict['text'] = token_dict['text'].replace(' ', '-')
            sentence_tokens.append(token_dict)
        sentences.append(sentence_tokens)
    return sentences

def brat_to_conll(text):
    output = ''
    sentences = get_sentences_and_tokens_from_spacy(text, spacy_nlp)
    for sentence in sentences:
        inside = False
        previous_token_label = 'O'
        for token in sentence:
            token['label'] = 'O'
            entity={'end':0}
            if token['label'] == 'O':
                gold_label = 'O'
                inside = False
            elif inside and token['label'] == previous_token_label:
                gold_label = 'I-{0}'.format(token['label'])
            else:
                inside = True
                gold_label = 'B-{0}'.format(token['label'])
            if token['end'] == entity['end']:
                inside = False
            previous_token_label = token['label']
            output += '{0} {1} {2} {3} {4}\n'.format(token['text'], '1', token['start'], token['end'], gold_label)

    return output
