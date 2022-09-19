#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import SplatStats as splat

hPath = '/home/chipdelmal/Documents/GitHub/s3s/'
###############################################################################
# Get filepaths
###############################################################################
hFolders = splat.getHistoryFolders(hPath)
hFiles = splat.getHistoryFiles(hFolders)
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
battle = splat.Battle(bDetail)
battle.alliedTeam
battle.getAllyByCategory('čħîþ ウナギ', category='player name')

# Export battle history -------------------------------------------------------
battle.dumpBattle('./BattlesData/')
###############################################################################
# Load Battle
###############################################################################
fName = splat.datetimeToString(battle.datetime)
battleLoaded = splat.loadBattle(f'./BattlesData/{fName}.pkl')

