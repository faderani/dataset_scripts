import argparse
import os.path
import json
import numpy as np
from sklearn.metrics import confusion_matrix as cm
from matplotlib.pylab import plt
import itertools
import pickle

from utils import *

parser = argparse.ArgumentParser(description='Draws confusion bar chart for input class.')


parser.add_argument('--pkpath', default='../SlowFast/outputs/sample.pickle', help='path to the prediction pickle file', required=True)
parser.add_argument('--outputdir', default='./outputs', help='path to the save dir', required=True)
parser.add_argument('--mode', default='total', help='total/noun/verb', required=False)
parser.add_argument('--annotdir', default='../../dataset_prep/output', help='path to annotaion dir', required=False)
parser.add_argument('--topk', default=5, help='Top K to appear in the bar chart', required=False, type=int)
parser.add_argument('--targetclass', default='Take bowl', help='Class to draw confusion bar chart', required=True)





def plot_bar(cmtx, save_path, class_names, trgt_cls, topk):
    class_idx = class_names.index(trgt_cls)
    row = np.append(cmtx[class_idx][0:class_idx], cmtx[class_idx][class_idx+1:])
    class_names = class_names[0:class_idx] + class_names[class_idx+1:]
    sorted_indices = np.argsort(row)[-topk:]
    save_path = os.path.join(save_path , f"{trgt_cls}.jpg")

    filtered_cls_names = []

    for x in sorted_indices:
        filtered_cls_names.append(class_names[x])

    # filtered_cls_names[2] = filtered_cls_names[2].replace("Divide/Pull Apart", "Divide\n")
    # filtered_cls_names[1] = filtered_cls_names[1].replace("Put", "Put\n")
    # filtered_cls_names[0] = filtered_cls_names[0].replace("Take", "Take\n")

    filtered_cls_names[2] = filtered_cls_names[2].replace("Cut", "Cut\n")
    filtered_cls_names[1] = filtered_cls_names[1].replace("Cut", "Cut\n")
    filtered_cls_names[0] = filtered_cls_names[0].replace("Put", "Put\n")

    values = row[sorted_indices]

    fig = plt.figure(figsize=(4,4))
    plt.bar(filtered_cls_names, values*100, width=0.8)

    plt.title(trgt_cls, fontsize=12)
    plt.ylabel('frequency (%)', fontsize=12)


    plt.xticks(fontsize=11)
    plt.tight_layout()
    plt.savefig(save_path)






if __name__ == "__main__":

    args = parser.parse_args()

    if os.path.exists(args.outputdir) == False:
        os.makedirs(args.outputdir)

    names_action, nouns_action, verbs_action = read_annots(args.annotdir)



    if args.mode == "total":
        class_names = names_action
    elif args.mode == "noun":
        class_names = nouns_action
    elif args.mode == "verb":
        class_names = verbs_action

    with open(args.pkpath, 'rb') as f:
        x = pickle.load(f)
    preds = np.argmax(x[0], axis=1).numpy()
    labels = np.argmax(x[1], axis=1).numpy()



    confusion_matrix = get_cm(args.annotdir, labels, preds, mode=args.mode, normalize="true")

    plot_bar(confusion_matrix, args.outputdir, class_names, args.targetclass, args.topk)