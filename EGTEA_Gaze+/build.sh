#!/bin/bash

DESTDIR=/ssd2/datasets1


VIDEO_CLIPS=$DESTDIR/video_clips.tar
if [ -f "$FILE" ]; then
    echo "$FILE exists." &
else
    wget -O $DESTDIR/video_clips.tar https://www.dropbox.com/s/udynz2u62wpdva6/video_clips.tar?dl=1 &
fi

tar -xf $DESTDIR/video_clips.tar &
python3 main.py --datadir $DESTDIR/cropped_clips --outputdir $DESTDIR/frames
