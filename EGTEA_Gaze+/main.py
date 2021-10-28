import argparse
import os

parser = argparse.ArgumentParser(description='Converting cropped videos to seperate frames')


parser.add_argument('--datapath', default='./cropped_videos', help='path to the root directory of videos', required=True)
parser.add_argument('--outputpath', default='output', help='path to output dir', required=True)
parser.add_argument('--p', action='store_false', help='to save data as numpy files')
parser.add_argument('--v', action='store_true', help='to visualize gaze data')



if __name__ == '__main__':
    args = parser.parse_args()

