import pickle
import numpy as np
import argparse
import os
import json

parser = argparse.ArgumentParser(description='Compares predictions and outputs to txt file')


parser.add_argument('--pkpath1', default='../SlowFast/outputs/sample.pickle', help='path to the first prediction pickle file', required=True)
parser.add_argument('--pkpath2', default='../SlowFast/outputs/sample.pickle', help='path to the second prediction pickle file', required=True)
parser.add_argument('--classname', default='Take bread', help='class name to compare', required=True)
parser.add_argument('--outputdir', default='./outputs', help='where to save text file', required=False)
parser.add_argument('--annotdir', default='../../dataset_prep/output', help='path to annotaion dir', required=False)


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

def compare_predictions(pkl_path1, pkl_path2, action_index, annot_dir):
    with open(pkl_path1, 'rb') as f:
        x = pickle.load(f)
    preds1 = np.argmax(x[0], axis=1).numpy()
    labels1 = np.argmax(x[1], axis=1).numpy()
    with open(pkl_path2, 'rb') as f:
        x = pickle.load(f)
    preds2 = np.argmax(x[0], axis=1).numpy()
    labels2 = np.argmax(x[1], axis=1).numpy()
    labels_indices = np.argwhere(labels1==action_index)
    sub_preds1 = preds1[labels_indices]
    sub_label1 = labels1[labels_indices]

    sub_preds2 = preds2[labels_indices]
    sub_label2 = labels2[labels_indices]
    csv_path = os.path.join(annot_dir, "test.csv")
    with open(csv_path, "r") as val:
        lines = val.readlines()
        for idx, x in enumerate(sub_label1):
            for line in lines:
                try:
                    video_idx = int(line.split(" ")[1])
                except:
                    continue
                if video_idx == labels_indices[idx]:
                    pth = line.split(" ")[3]
                    print \
                        (f"True Label={x}, Pred1={preds1[labels_indices[idx]]}, Pred2={preds2[labels_indices[idx]]} -- {pth}")
                    break

if __name__ == '__main__':
    args = parser.parse_args()

    if os.path.exists(args.outputdir) == False:
        os.makedirs(args.outputdir)


    names_action,_,_ = read_annots(args.annotdir)

    compare_predictions(args.pkpath1, args.pkpath2,
                        names_action.index(args.classname) + 1, args.annotdir)