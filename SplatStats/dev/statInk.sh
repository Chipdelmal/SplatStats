#!/bin/bash

for six in {0..2}
do
    echo "* Processing $six All (base)" 
    python statInk.py "$six" "All" 0
    for gmod in "All" "Clam Blitz" "Splat Zones" "Tower Control" "Turf War" "Rainmaker"
    do
        echo "* Processing $six $gmod"
        python statInk.py "$six" "$gmod" 1
    done
    python statInkPanel.py "$six"
done