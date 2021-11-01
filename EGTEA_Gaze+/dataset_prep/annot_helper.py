import argparse
import os

parser = argparse.ArgumentParser(description='Preparing annotations for EGTEA Gaze+ datasets. Converts annotations formats making it readable by slowfast dataloader and removes non hand held object classes')


parser.add_argument('--splitpath', default='./trainsplit.txt', help='path to the original train split text file', required=True)
parser.add_argument('--datasetroot', default='./frames', help='path to the dataset root', required=True)
parser.add_argument('--outputdir', default='./output', help='path to output dir', required=False)
parser.add_argument('--actionidxpath', default='./splits/action_idx.txt', help='path to action idx file', required=False)
parser.add_argument('--ignore', default='./splits/ignore_idx.txt', help='path to ignore file', required=False)



def create_new_nounverb_idx(outputdir):
    actionidxpath = os.path.join(outputdir, "reduced_action_idx.txt")
    nounoutputpath = os.path.join(outputdir, "reduced_noun_idx.txt")
    verboutputpath = os.path.join(outputdir, "reduced_verb_idx.txt")

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
                        cnt_n+=1
                        noun_stack.append(noun)
                    if verb not in verb_stack:
                        new_verb_idx.write(f"{verb} {cnt_v}\n")
                        cnt_v+=1
                        verb_stack.append(verb)





def create_new_action_idx(actionidxpath, ignore, outputdir):

    outputpath = os.path.join(outputdir, "reduced_action_idx.txt")
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
                        cnt+=1

def get_ignore_idx(ignore):
    indices = []
    with open(ignore, "r") as ignore:
        lines = ignore.readlines()
        for line in lines:
            line = line.strip("\n")
            idx = line.split(" ")[-1]
            indices.append(idx)

    return indices

def convert(txt_path, ignore_path, dataset_root, out_dir):

    ignore_indices = get_ignore_idx(ignore_path)

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

    create_new_action_idx(args.actionidxpath, args.ignore, args.outputdir)
    #convert(args.splitpath, args.ignore ,args.datasetroot, args.outputdir)
    create_new_nounverb_idx(args.outputdir)