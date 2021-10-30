#!/bin/bash

DESTDIR=./
DESTPATH= ./kinetics400/I3D_8x8_R50.pkl


if [ -f "$DESTPATH" ]; then
    echo "$DESTPATH exists."
else
    curl https://dl.fbaipublicfiles.com/pyslowfast/model_zoo/kinetics400/I3D_8x8_R50.pkl --create-dirs -o ./kinetics400/I3D_8x8_R50.pkl
fi
