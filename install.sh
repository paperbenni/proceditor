#!/usr/bin/env bash

for i in ~/.config/blender/*; do

    [ -d "$i" ] || continue
    OUTPATH="$i/scripts/addons/proceditor"
    [ -e "$OUTPATH" ] || mkdir -p "$OUTPATH" || exit 1
    echo "installing to $OUTPATH"
    cp -r ./* "$OUTPATH"/

done
