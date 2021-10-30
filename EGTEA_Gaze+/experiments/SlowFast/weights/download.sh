#!/bin/bash

DESTDLPATH= ./kinetics400/SLOWFAST_8x8_R50.pkl


if [ -f "$DESTDLPATH" ]; then
    echo "$DESTDLPATH exists."
else
    curl https://dl.fbaipublicfiles.com/pyslowfast/model_zoo/kinetics400/SLOWFAST_8x8_R50.pkl --create-dirs -o ./kinetics400/SLOWFAST_8x8_R50.pkl
fi

