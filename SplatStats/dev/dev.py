#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pandas as pd
from os import path
import SplatStats as splat
import matplotlib.pyplot as plt

(iPath, oPath) = (
    '/home/chipdelmal/Documents/GitHub/s3s/',
    '/home/chipdelmal/Documents/GitHub/SplatStats/BattlesData'
)
###############################################################################
# Create Player Objects
###############################################################################
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPathsDumped = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPathsRead = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
chip = splat.Player('čħîþ ウナギ', 7293)
yami = splat.Player('Yami ウナギ', None)
april = splat.Player('April ウナギ', None)
richie = splat.Player('Riché ウナギ', None)
memo = splat.Player('Oswal　ウナギ', None)
tomas = splat.Player('Murazee', None)
# Group players for iterations ------------------------------------------------
team = (chip, yami, april, richie, memo, tomas)






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

###############################################################################
# Violin Plot
###############################################################################
# Create history object
history = splat.History(iPath, oPath)
# Get the battles filepaths
playerHistory = history.getPlayerHistory('čħîþ ウナギ')
validMatches = playerHistory[playerHistory['win']!='NA']
(fig, ax) = plt.subplots()
vp = ax.violinplot(
    [
        list(validMatches['kill']), 
        list(validMatches['death'])
    ], [2, 4], 
    widths=2, showmeans=True, showmedians=False, showextrema=True
)
sum(validMatches['kill'])/sum(validMatches['death'])

playerHistory.to_csv(path.join(oPath, 'chipHistory.csv'))
battleFiles = history.battleFilepaths