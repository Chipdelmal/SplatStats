#!/bin/bash

DTA_PTH="/home/chipdelmal/Documents/GitHub/s3s/"
BTL_PTH="/home/chipdelmal/Documents/Sync/BattlesData/"
###############################################################################
# Run scripts
###############################################################################
bash "${DTA_PTH}downloadJSON.sh" -o
# python main.py $DTA_PTH $BTL_PTH
# python scatterDev.py $DTA_PTH $BTL_PTH
python plotsMain.py $DTA_PTH $BTL_PTH
python plotsTeam.py $DTA_PTH $BTL_PTH