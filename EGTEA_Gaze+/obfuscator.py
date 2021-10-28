import argparse
import os
import glob
import numpy as np
import cv2
import matplotlib.pyplot as plt
from utilities import my_pool
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Obfuscating images using hand-obj masks npy files')


parser.add_argument('--datadir', default='./frames', help='path to the root directory of images', required=True)
parser.add_argument('--maskdir', default='./hand_obj_npy', help='path to the root directory of mask npy files', required=True)
parser.add_argument('--outputdir', default='output', help='path to output dir', required=True)


def get_all_images(root_path):
    """Returns absolute pathes to all images in root_path dir and subdirs"""
    all_jpg_files = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".jpg"):
                all_jpg_files.append(os.path.join(root, file))

    return all_jpg_files


def run_obfuscation_hand_plus_object(jpg_paths, mask_paths, output_dir,dilation_size=0):
    dilate_kernel = np.ones((dilation_size, dilation_size), dtype=bool)
    print(kernel_size)
    print("=============")
    for idx, jpg_path in enumerate(jpg_paths):
        if idx % 100 == 0:
            print("===>", int(idx / len(jpg_paths) * 100))

        hand_npy_file = os.path.join(mask_paths, *jpg_paths.split("/")[-3,])
        obj_npy_file = os.path.join(mask_paths, *jpg_paths.split("/")[-3,])

        hand_file_name = hand_npy_file.split("/")[-1].split(".")[0] + "_hand" + ".npy"
        obj_file_name = hand_npy_file.split("/")[-1].split(".")[0] + "_obj" + ".npy"

        hand_npy_file = hand_npy_file.split("/")[0:-1] + [hand_file_name]
        obj_npy_file = obj_npy_file.split("/")[0:-1] + [obj_file_name]

        hand_npy_file = os.path.join(*hand_npy_file)
        obj_npy_file = os.path.join(*obj_npy_file)

        try:
            hand_bbox = np.load(hand_npy_file)
        except:
            hand_bbox = []
        try:
            obj_bbox = np.load(obj_npy_file)
        except:
            obj_bbox = []

        #         print(hand_bbox)
        #         print(obj_bbox.shape)

        save_path = os.path.join(output_dir,str(dilation_size) ,*jpg_paths.split("/")[-3,])


        if os.path.exists(save_path):
            continue

        img = cv2.imread(jpg_path)
        #         print(img.shape)

        obf_img = np.zeros(img.shape)

        for bbox in hand_bbox:
            score = bbox[4]
            if score > 0.8:
                x1, y1, x2, y2 = bbox[0:4].astype(np.uint64)

                x1 = int(max(x1 - dilation_size / 2, 0))
                y1 = int(max(y1 - dilation_size / 2, 0))
                x2 = int(min(x2 + dilation_size / 2, img.shape[1]))
                y2 = int(min(y2 + dilation_size / 2, img.shape[0]))

                obf_img[y1:y2, x1:x2] = img[y1:y2, x1:x2]
        for bbox in obj_bbox:
            score = bbox[4]
            if score > 0.8:
                x1, y1, x2, y2 = bbox[0:4].astype(np.uint64)

                x1 = int(max(x1 - dilation_size / 2, 0))
                y1 = int(max(y1 - dilation_size / 2, 0))
                x2 = int(min(x2 + dilation_size / 2, img.shape[1]))
                y2 = int(min(y2 + dilation_size / 2, img.shape[0]))

                obf_img[y1:y2, x1:x2] = img[y1:y2, x1:x2]

        if os.path.exists(os.path.join(*save_path.split("/")[0:-1])) == False:
            os.makedirs(os.path.join(*save_path.split("/")[0:-1]))

        cv2.imwrite(save_path, obf_img)





if __name__ == '__main__':
    args = parser.parse_args()
    jpg_paths = get_all_images(args.datadir)
    run_obfuscation_hand_plus_object(jpg_paths, args.maskdir, args.outputdir)