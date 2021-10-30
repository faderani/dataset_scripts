#!/bin/bash

DESTDIR=./
DESTPATH= ./kinetics400/SLOWFAST_8x8_R50.pkl


if [ -f "$DESTPATH" ]; then
    echo "$DESTPATH exists."
else
    curl https://dl.fbaipublicfiles.com/pyslowfast/model_zoo/kinetics400/SLOWFAST_8x8_R50.pkl --create-dirs -o $DESTPATH
fi

