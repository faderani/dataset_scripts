#!/bin/bash

DESTDIR=/ssd2/datasets/EGTEA_Gaze++


VIDEO_CLIPS=$DESTDIR/video_clips.tar
HANDS_OBJS=$DESTDIR/hands_obj_npy.zip


if [ -f "$VIDEO_CLIPS" ]; then
    echo "$VIDEO_CLIPS exists."
else
    wget -O $VIDEO_CLIPS https://www.dropbox.com/s/udynz2u62wpdva6/video_clips.tar?dl=1
fi

if [ -f "$HANDS_OBJS" ]; then
    echo "$HANDS_OBJS exists."
else
    wget -O $HANDS_OBJS https://www.dropbox.com/s/iyd3flhjfrqqyr6/hand_plus_object_npy_compressed.zip?dl=1
fi

tar -xf $VIDEO_CLIPS -C $DESTDIR
unzip $HANDS_OBJS -d $DESTDIR


python3.8 vid_to_img.py --datadir $DESTDIR/cropped_clips --outputdir $DESTDIR/frames
python3.8 obfuscator.py --datadir $DESTDIR/frames --maskdir $DESTDIR/hand_plus_object_npy --outputdir $DESTDIR/hand_obj_obfuscated
