import argparse
import os.path
import json
import numpy as np
from sklearn.metrics import confusion_matrix as cm
from matplotlib.pylab import plt
import itertools
import pickle



def read_annots(dir):
    names_action_path = os.path.join(dir, "reduced_action_idx.json")
    nouns_action_path = os.path.join(dir, "reduced_noun_idx.json")
    verbs_action_path = os.path.join(dir, "reduced_verb_idx.json")

    with open(names_action_path) as json_file:
        names_action = json.load(json_file)
        names_action = list(names_action.keys())
    with open(nouns_action_path) as json_file:
        nouns_action = json.load(json_file)
        nouns_action = list(nouns_action.keys())
    with open(verbs_action_path) as json_file:
        verbs_action = json.load(json_file)
        verbs_action = list(verbs_action.keys())

    return names_action, nouns_action, verbs_action



def get_cm(dir, labels, preds, mode="total", normalize=None):
    verb_mapper_path = os.path.join(dir, "mapping_verb.json")
    noun_mapper_path = os.path.join(dir, "mapping_noun.json")

    if "verb" in mode:
        with open(verb_mapper_path) as json_file:
            v_map = json.load(json_file)
            for key, value in v_map.items():
                preds = np.where(preds == int(key), value, preds)
                labels = np.where(labels == int(key), value, labels)
    elif "noun" in mode:
        with open(noun_mapper_path) as json_file:
            n_map = json.load(json_file)
            for key, value in n_map.items():
                preds = np.where(preds == int(key), value, preds)
                labels = np.where(labels == int(key), value, labels)

    return cm(labels, preds, normalize=normalize)