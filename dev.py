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
# Load file
#   fName = '/home/chipdelmal/Documents/GitHub/s3s/export-1663442390/results.json'
#   fName = '/home/chipdelmal/Documents/GitHub/s3s/export-1663524543/results.json'
###############################################################################
fName = hFiles[0]
with open(fName, 'r') as file:
    data = json.load(file)
histSize = len(data)
###############################################################################
# Explore operations
###############################################################################
i = 0
bDetail = data[i]['data']['vsHistoryDetail']
# Process battle history ------------------------------------------------------
battle = bat.Battle(bDetail)
battle.awards
# Export battle history -------------------------------------------------------
battle.dumpBattle('./Battles/')
###############################################################################
# Load Battle
###############################################################################
fName = aux.datetimeToString(battle.datetime)
battleLoaded = aux.loadBattle(f'./Battles/{fName}.pkl')
