import os
import numpy as np
import src.utils_nlp as utils_nlp


def remap_labels(y_pred, y_true, dataset, evaluation_mode='bio'):
    '''
    y_pred: list of predicted labels
    y_true: list of gold labels
    evaluation_mode: 'bio', 'token', or 'binary'

    Both y_pred and y_true must use label indices and names specified in the dataset
#     (dataset.unique_label_indices_of_interest, dataset.unique_label_indices_of_interest).
    '''
    all_unique_labels = dataset.unique_labels
    if evaluation_mode == 'bio':
        # sort label to index
        new_label_names = all_unique_labels[:]
        new_label_names.remove('O')
        new_label_names.sort(key=lambda x: (utils_nlp.remove_bio_from_label_name(x), x))
        new_label_names.append('O')
        new_label_indices = list(range(len(new_label_names)))
        new_label_to_index = dict(zip(new_label_names, new_label_indices))

        remap_index = {}
        for i, label_name in enumerate(new_label_names):
            label_index = dataset.label_to_index[label_name]
            remap_index[label_index] = i

    elif evaluation_mode == 'token':
        new_label_names = set()
        for label_name in all_unique_labels:
            if label_name == 'O':
                continue
            new_label_name = utils_nlp.remove_bio_from_label_name(label_name)
            new_label_names.add(new_label_name)
        new_label_names = sorted(list(new_label_names)) + ['O']
        new_label_indices = list(range(len(new_label_names)))
        new_label_to_index = dict(zip(new_label_names, new_label_indices))

        remap_index = {}
        for label_name in all_unique_labels:
            new_label_name = utils_nlp.remove_bio_from_label_name(label_name)
            label_index = dataset.label_to_index[label_name]
            remap_index[label_index] = new_label_to_index[new_label_name]

    elif evaluation_mode == 'binary':
        new_label_names = ['NAMED_ENTITY', 'O']
        new_label_indices = [0, 1]
        new_label_to_index = dict(zip(new_label_names, new_label_indices))

        remap_index = {}
        for label_name in all_unique_labels:
            new_label_name = 'O'
            if label_name != 'O':
                new_label_name = 'NAMED_ENTITY'
            label_index = dataset.label_to_index[label_name]
            remap_index[label_index] = new_label_to_index[new_label_name]

    else:
        raise ValueError("evaluation_mode must be either 'bio', 'token', or 'binary'.")

    new_y_pred = [ remap_index[label_index] for label_index in y_pred ]
    new_y_true = [ remap_index[label_index] for label_index in y_true ]

    new_label_indices_with_o = new_label_indices[:]
    new_label_names_with_o = new_label_names[:]
    new_label_names.remove('O')
    new_label_indices.remove(new_label_to_index['O'])

    return new_y_pred, new_y_true, new_label_indices, new_label_names, new_label_indices_with_o, new_label_names_with_o