import argparse
import os
import json

parser = argparse.ArgumentParser(description='Preparing annotations for EGTEA Gaze+ datasets. Converts annotations formats making it readable by slowfast dataloader and removes non hand held object classes')


parser.add_argument('--splitpath', default='./trainsplit.txt', help='path to the original train split text file', required=True)
parser.add_argument('--datasetroot', default='./frames', help='path to the dataset root', required=True)
parser.add_argument('--task', default='convert', help='convert/newidx', required=True)
parser.add_argument('--outputdir', default='./output', help='path to output dir', required=False)
parser.add_argument('--actionidxpath', default='./splits/action_idx.txt', help='path to action idx file', required=False)
parser.add_argument('--ignore', default='./splits/ignore_idx.txt', help='path to ignore file', required=False)
parser.add_argument('--merge', default='./splits/merge.json', help='path to merge file', required=False)



def create_mapper(outputdir, mode="verb"):
    mode_path = os.path.join(outputdir, f"reduced_{mode}_idx.txt")
    actionidxpath = os.path.join(outputdir, "reduced_action_idx.txt")
    out_path = os.path.join(outputdir, f'mapping_{mode}.json')

    actions = {}
    action_idx = {}
    with open(mode_path) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip("\n")
            f = " ".join(line.split(" ")[:-1])
            s = line.split(" ")[-1]
            actions[f] = int(s)

    with open(actionidxpath) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip("\n")
            f = " ".join(line.split(" ")[:-1])
            s = line.split(" ")[-1]
            action_idx[f] = int(s)

    mapping = {}

    if "verb" in mode:
        for key1, value1 in action_idx.items():
            for key2, value2 in actions.items():
                new_key1 = " ".join(key1.split(" ")[0:-1])
                if new_key1 == key2:
                    mapping[str(value1)] = value2
    else:
        for key1, value1 in action_idx.items():
            for key2, value2 in actions.items():
                new_key1 = key1.split(" ")[-1]
                if new_key1 == key2:
                    mapping[str(value1)] = value2

    with open(out_path, "w") as json_file:
        json.dump(mapping, json_file)

def create_new_nounverb_idx(outputdir):
    actionidxpath = os.path.join(outputdir, "reduced_action_idx.txt")
    nounoutputpath = os.path.join(outputdir, "reduced_noun_idx.txt")
    verboutputpath = os.path.join(outputdir, "reduced_verb_idx.txt")

    outputpathjson_n = os.path.join(outputdir, "reduced_noun_idx.json")
    outputpathjson_v = os.path.join(outputdir, "reduced_verb_idx.json")
    json_out_n = {}
    json_out_v = {}

    noun_stack = []
    verb_stack = []

    cnt_n = 1
    cnt_v = 1

    with open(nounoutputpath, "w") as new_noun_idx:
        with open(verboutputpath, "w") as new_verb_idx:
            with open(actionidxpath, "r") as action_idx:
                lines = action_idx.readlines()
                for line in lines:
                    line = line.strip("/n")

                    noun = line.split(" ")[-2]
                    verb = " ".join(line.split(" ")[:-2])

                    if noun not in noun_stack:
                        new_noun_idx.write(f"{noun} {cnt_n}\n")
                        json_out_n[noun] = cnt_n
                        cnt_n+=1
                        noun_stack.append(noun)
                    if verb not in verb_stack:
                        new_verb_idx.write(f"{verb} {cnt_v}\n")
                        json_out_v[verb] = cnt_n
                        cnt_v+=1
                        verb_stack.append(verb)

    with open(outputpathjson_n, "w") as json_file:
        json.dump(json_out_n, json_file)
    with open(outputpathjson_v, "w") as json_file:
        json.dump(json_out_v, json_file)



def create_new_action_idx(actionidxpath, ignore, outputdir):

    outputpath = os.path.join(outputdir, "reduced_action_idx.txt")
    outputpathjson = os.path.join(outputdir, "reduced_action_idx.json")
    json_out = {}
    cnt = 1
    with open(outputpath, "w") as new_action_idx:
        with open(actionidxpath, "r") as old_action_idx:
            with open(ignore, "r") as ignore:

                lines1 = old_action_idx.readlines()
                lines2 = ignore.readlines()

                for line1 in lines1:
                    line1 = line1.strip("\n")
                    flg = True
                    for line2 in lines2:
                        line2 = line2.strip("\n")
                        if line2 in line1:
                            flg = False
                            break
                    if flg:
                        new_action_idx.write(" ".join(line1.split(" ")[0:-1]) + " " + str(cnt) + "\n")
                        json_out[" ".join(line1.split(" ")[0:-1])] = cnt
                        cnt+=1
    with open(outputpathjson, "w") as json_file:
        json.dump(json_out, json_file)


def get_ignore_idx(ignore):
    indices = []
    with open(ignore, "r") as ignore:
        lines = ignore.readlines()
        for line in lines:
            line = line.strip("\n")
            idx = line.split(" ")[-1]
            indices.append(idx)

    return indices

def get_merge_dict(merge):
    indices = []
    with open(merge, "r") as json_file:
        return json.load(json_file)

def convert(txt_path, ignore_path, merge_path, dataset_root, out_dir):

    ignore_indices = get_ignore_idx(ignore_path)
    merge_dict = get_merge_dict(merge_path)

    out_split_path = os.path.join(out_dir, txt_path.split("/")[-1].split(".")[0] + ".csv")
    action_idx_path = os.path.join(out_dir, "action_idx.txt")

    cnt = 1
    old_idx = 0
    new_idx = 0
    vid_id = -1

    with open(txt_path, "r") as split:
        lines = split.readlines()
        with open(out_split_path, "w") as modified_split:

            modified_split.write("original_vido_id video_id frame_id path labels\n")

            for idx1, line in enumerate(lines):

                line = line.strip("\n")
                arr = line.split(" ")
                sub_dir_name, action_idx = arr[0], arr[1]
                dir_name = "-".join(sub_dir_name.split("-")[0:3])

                if int(action_idx) < int(old_idx):    
                    cnt = 1
                    old_idx = 0
                    new_idx = 0

                if action_idx in ignore_indices:
                    if action_idx in merge_dict.keys():
                        vid_id +=1
                        jpgs = os.listdir(os.path.join(dataset_root, dir_name, sub_dir_name))
                        for idx2 in range(1, len(jpgs) + 1):
                            s = sub_dir_name + " " + str(vid_id) + " " + str(
                                idx2 - 1) + " " + dir_name + "/" + sub_dir_name + "/" + f"{idx2}.jpg" + " " + f"\"{merge_dict[action_idx]}\"" + "\n"
                            modified_split.write(s)
                    continue
                vid_id +=1
                new_idx = action_idx    
                if old_idx == 0:
                    old_idx = new_idx
                if old_idx != new_idx:
                    cnt+=1

                old_idx = new_idx
                
                jpgs = os.listdir(os.path.join(dataset_root, dir_name, sub_dir_name))
                for idx2 in range(1, len(jpgs) + 1):
                    s = sub_dir_name + " " + str(vid_id) + " " + str(
                        idx2 - 1) + " " + dir_name + "/" + sub_dir_name + "/" + f"{idx2}.jpg" + " " + f"\"{cnt}\"" + "\n"
                    modified_split.write(s)
                

if __name__ == '__main__':
    args = parser.parse_args()

    if os.path.exists(args.outputdir) == False:
        os.makedirs(args.outputdir)

    if args.task == 'convert':
        create_new_action_idx(args.actionidxpath, args.ignore, args.outputdir)
        convert(args.splitpath, args.ignore, args.merge ,args.datasetroot, args.outputdir)
    else:
        create_new_action_idx(args.actionidxpath, args.ignore, args.outputdir)
        create_new_nounverb_idx(args.outputdir)
        create_mapper(args.outputdir, mode="noun")
        create_mapper(args.outputdir, mode="verb")