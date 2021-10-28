#!/bin/bash

DESTDIR=/ssd2/datasets1

wget -O $DESTDIR/video_clips.tar https://www.dropbox.com/s/udynz2u62wpdva6/video_clips.tar?dl=1
tar -xf $DESTDIR/video_clips.tar
python3 main.py --datadir $DESTDIR/cropped_clips --outputdir $DESTDIR/frames
