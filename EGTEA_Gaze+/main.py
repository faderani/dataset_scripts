import argparse
import os

parser = argparse.ArgumentParser(description='Converting cropped videos to seperate frames')


parser.add_argument('--datadir', default='./cropped_videos', help='path to the root directory of videos', required=True)
parser.add_argument('--outputdir', default='output', help='path to output dir', required=True)

def vids_to_img(vid_root, outputdir):
    all_mp4_files = []
    for root, dirs, files in os.walk(vid_root):
        for file in files:
            if file.endswith(".mp4"):
                all_mp4_files.append(os.path.join(root, file))

    for mp4 in all_mp4_files:


        directory = mp4.replace(".mp4", "").split("/")[-2:]
        directory = os.path.join(outputdir, *directory)

        if os.path.exists(directory) == False:
            os.makedirs(directory)

        command = f"ffmpeg -i {mp4} -qscale:v 2  {directory}/%d.jpg"

        os.system(command)


if __name__ == '__main__':
    args = parser.parse_args()

    vids_to_img(args.datadir, args.outputdir)




