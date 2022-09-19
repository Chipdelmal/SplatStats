#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import Battle as bat
import auxiliary as aux

hPath = '/home/chipdelmal/Documents/GitHub/s3s/'
###############################################################################
# Get filepaths
###############################################################################
hFolders = aux.getHistoryFolders(hPath)
hFiles = aux.getHistoryFiles(hFolders)
###############################################################################
# Load File
###############################################################################
fName = hFiles[6]
with open(fName, 'r') as file:
    data = json.load(file)
histSize = len(data)
###############################################################################
# Explore operations
###############################################################################
for i in range(histSize):
    bDetail = data[i]['data']['vsHistoryDetail']
    # Process battle history --------------------------------------------------
    battle = bat.Battle(bDetail)
    battle.alliedTeam
    # Export battle history ---------------------------------------------------
    battle.dumpBattle('./Battles/')