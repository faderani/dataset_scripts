import argparse
import os.path
import json
import numpy as np
from sklearn.metrics import confusion_matrix as cm
from matplotlib.pylab import plt
import itertools
import pickle



parser = argparse.ArgumentParser(description='Draws confusion matrices')


parser.add_argument('--pkpath', default='../SlowFast/outputs/sample.pickle', help='path to the prediction pickle file', required=True)
parser.add_argument('--outputdir', default='./output', help='path to the save dir', required=True)
parser.add_argument('--mode', default='total', help='total/noun/verb', required=False)
parser.add_argument('--annotdir', default='../../dataset_prep/output', help='path to annotaion dir', required=False)
parser.add_argument('--ignoretest', default='../../dataset_prep/splits/ignore_test.txt', help='path to ignoring idx at test time', required=False)



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

def get_accuracy(cm):
    list_acc = []
    for i in range(len(cm)):
        acc = 0
        if cm[i,:].sum() > 0:
            acc = cm[i,i]/cm[i,:].sum()
        list_acc.append(acc)

    return 100*np.mean(list_acc), 100*np.trace(cm)/np.sum(cm)


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


def plot_cm(cmtx, save_path, class_names, mode):

    save_path = os.path.join(save_path, mode + ".jpg")

    #class_names = [str(i) for i in range(class_num)]

    figure = plt.figure(figsize=(int(.7*len(class_names)),int(.7*len(class_names))))
    plt.imshow(cmtx, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Confusion matrix")
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=90)
    plt.yticks(tick_marks, class_names)

    # Use white text if squares are dark; otherwise black.
    threshold = cmtx.max() / 2.0
    for i, j in itertools.product(range(cmtx.shape[0]), range(cmtx.shape[1])):
        color = "white" if cmtx[i, j] > threshold else "black"
        plt.text(
            j,
            i,
            format(cmtx[i, j], ".2f") if cmtx[i, j] != 0 else "0",
            horizontalalignment="center",
            color=color,
        )

    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.savefig(save_path)
    #plt.show()


if __name__ == '__main__':
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
    plot_cm(confusion_matrix,args.outputdir, class_names, args.mode)

    mean_class_acc, acc = get_accuracy(get_cm(args.annotdir, labels, preds, mode=args.mode, normalize=None))
    print('mean acc: %.2f, acc: %.2f' % (mean_class_acc, acc))



