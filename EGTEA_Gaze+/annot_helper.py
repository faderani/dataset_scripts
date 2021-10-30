import argparse
import os

parser = argparse.ArgumentParser(description='Preparing annotations for EGTEA Gaze+ datasets. Converts annotations formats making it readable by slowfast dataloader and removes non hand held object classes')


parser.add_argument('--splitpath', default='./trainsplit.txt', help='path to the original train split text file', required=True)
parser.add_argument('--datasetroot', default='./frames', help='path to the dataset root', required=True)
parser.add_argument('--outputdir', default='./output', help='path to output dir', required=False)

parser.add_argument('--ignore', default='./ignore.txt', help='path to output dir', required=False)





def convert(txt_path, dataset_root, out_path):

    out_path = os.path.join(out_path, txt_path.split("/")[-1].split(".")[0] + ".csv")

    with open(txt_path, "r") as split:
        lines = split.readlines()
        with open(out_path, "w") as modified_split:

            modified_split.write("original_vido_id video_id frame_id path labels\n")

            for idx1, line in enumerate(lines):
                line = line.strip("\n")
                arr = line.split(" ")
                sub_dir_name, action_idx = arr[0], arr[1]
                dir_name = "-".join(sub_dir_name.split("-")[0:3])

                jpgs = os.listdir(os.path.join(dataset_root, dir_name, sub_dir_name))
                for idx2 in range(1, len(jpgs) + 1):
                    s = sub_dir_name + " " + str(idx1) + " " + str(
                        idx2 - 1) + " " + dir_name + "/" + sub_dir_name + "/" + f"{idx2}.jpg" + " " + f"\"{action_idx}\"" + "\n"
                    modified_split.write(s)

if __name__ == '__main__':
    args = parser.parse_args()

    convert(args.splitpath, args.datasetroot, args.outputdir)