#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pandas as pd
from os import path
import SplatStats as splat

(iPath, oPath) = (
    '/home/chipdelmal/Documents/GitHub/s3s/',
    '/home/chipdelmal/Documents/GitHub/SplatStats/BattlesData'
)
history = splat.History(iPath, oPath)
history.getBattleFilepaths()
playerHistory = history.getPlayerAlliedHistory('čħîþ ウナギ')
playerHistory.to_csv(path.join(oPath, 'chipHistory.csv'))

battleFiles = history.battleFilepaths
# Iterate through battles -----------------------------------------------------
playerDFs = []
for batFile in battleFiles:
    battle = splat.loadBattle(batFile)
    row = battle.getAllyByCategory('čħîþ ウナギ', category='player name')
    playerDFs.append(row)
player = pd.concat(playerDFs, axis=0)
player = player.reset_index(drop=True)
player = player.drop(['player name', 'player name id'], axis=1)
player = player.drop_duplicates()
player
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
i = 0
bDetail = data[i]['data']['vsHistoryDetail']
# Process battle history ------------------------------------------------------
battle = splat.Battle(bDetail)
battle.enemyTeams
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

