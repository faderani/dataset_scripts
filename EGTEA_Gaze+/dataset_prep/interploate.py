

import argparse
import os
import numpy as np
import cv2
from natsort import natsorted
from shutil import copy

from tqdm import tqdm

parser = argparse.ArgumentParser(description='replacing blank images via interpolation')
parser.add_argument('--datadir', default='./frames', help='path to the root directory of images', required=True)
parser.add_argument('--outputdir', default='/0_interpolated/', help='path to output dir', required=False)


def get_all_jpg_files(root):
    all_jpg_files = []
    for root, dirs, files in os.walk(root):
            for file in files:
                if file.endswith(".jpg"):
                    all_jpg_files.append(os.path.join(root, file))



    return all_jpg_files

def copy_jpg_file(dst, src, dir):
    dst = dst.replace("/0/", dir)
    dst_dir = os.path.join("/",*dst.split("/")[0:-1])
    if os.path.exists(dst_dir) == False:
        os.makedirs(dst_dir)
    copy(src, dst)

def interpolate(all_jpg_files, outdir):

    for jpg_file in tqdm(all_jpg_files):

        size = os.path.getsize(jpg_file)
        if size!=5427:
            copy_jpg_file(jpg_file, jpg_file, outdir)
            continue

        dir = os.path.join("/",*jpg_file.split("/")[0:-1])





        index = int(jpg_file.split("/")[-1].split(".")[0])


        forward_index = index+1
        backward_index = index-1
        forward_path = os.path.join(dir, f"{index+1}.jpg")
        backward_path = os.path.join(dir, f"{index-1}.jpg")


        while os.path.exists(forward_path):
            size = os.path.getsize(forward_path)
            if size != 5427:
                break
            forward_index += 1
            forward_path = os.path.join(dir, f"{forward_index}.jpg")

        while os.path.exists(backward_path):
            size = os.path.getsize(backward_path)
            if size != 5427:
                break
            backward_index -= 1
            backward_path = os.path.join(dir, f"{backward_index}.jpg")



        if os.path.exists(forward_path) == False and os.path.exists(backward_path) != False:
            path = os.path.join(dir, f"{backward_index}.jpg")
            # print("forward", path.split("/")[-2:], jpg_file.split("/")[-2:])
            copy_jpg_file(jpg_file, path, outdir)

        elif os.path.exists(backward_path) == False and os.path.exists(forward_path) != False:
            path = os.path.join(dir, f"{forward_index}.jpg")
            # print("backward", path.split("/")[-2:], jpg_file.split("/")[-2:])
            copy_jpg_file(jpg_file, path, outdir)
        elif os.path.exists(backward_path) == False and os.path.exists(forward_path) == False:
            path = os.path.join(dir, f"{index}.jpg")
            # print("as is",path.split("/")[-2:], jpg_file.split("/")[-2:])
            copy_jpg_file(jpg_file, path, outdir)
        elif abs(index - backward_index) <= abs(index - forward_index) :
            path = os.path.join(dir, f"{backward_index}.jpg")
            #print("forward",path.split("/")[-2:], jpg_file.split("/")[-2:])
            copy_jpg_file(jpg_file, path, outdir)
        elif abs(index - backward_index) > abs(index - forward_index):
            path = os.path.join(dir, f"{forward_index}.jpg")
            #print("backward",path.split("/")[-2:], jpg_file.split("/")[-2:])
            copy_jpg_file(jpg_file, path, outdir)
        else:
            path = os.path.join(dir, f"{index}.jpg")
            #print("as is",path.split("/")[-2:], jpg_file.split("/")[-2:])
            copy_jpg_file(jpg_file, path, outdir)





if __name__ == '__main__':
    args = parser.parse_args()
    blank_jpg_files = get_all_jpg_files(args.datadir)
    interpolate(blank_jpg_files, args.outputdir)