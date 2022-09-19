#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pandas as pd
from os import path
import SplatStats as splat


# Demo names:
#   čħîþ ウナギ, Yami ウナギ, April ウナギ, Riché ウナギ, Oswal　ウナギ, Murazee

(iPath, oPath) = (
    '/home/chipdelmal/Documents/GitHub/s3s/',
    '/home/chipdelmal/Documents/GitHub/SplatStats/BattlesData'
)
history = splat.History(iPath, oPath)
history.getBattleFilepaths()
playerHistory = history.getPlayerHistory('čħîþ ウナギ')
playerHistory

playerHistory.to_csv(path.join(oPath, 'chipHistory.csv'))

battleFiles = history.battleFilepaths





###############################################################################
# Get filepaths
###############################################################################
hFolders = splat.getHistoryFolders(iPath)
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
i = 8
bDetail = data[i]['data']['vsHistoryDetail']
# Process battle history ------------------------------------------------------
battle = splat.Battle(bDetail)
battle.alliedTeam
battle.getPlayerByCategory('čħîþ ウナギ', battle.alliedTeam, category='player name')
battle.getAllyByCategory('čħîþ ウナギ', category='player name')
battle.getEnemyByCategory('CHIPPI', category='player name')[0]

awards = battle.awards


# Export battle history -------------------------------------------------------
battle.dumpBattle('./BattlesData/')
###############################################################################
# Load Battle
###############################################################################
fName = splat.datetimeToString(battle.datetime)
battleLoaded = splat.loadBattle(f'./BattlesData/{fName}.pkl')

