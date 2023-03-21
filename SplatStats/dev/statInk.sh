#!/bin/bash

for six in {0..2}
do
    for gmod in "All" "Clam Blitz" "Splat Zones" "Tower Control" "Turf War" "Rainmaker"
    do
        echo "* Processing $six $gmod"
        python statInk.py "$six" "$gmod"
    done
    python statInkPanel.py "$six"
done