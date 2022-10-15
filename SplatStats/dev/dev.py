#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pandas as pd
from os import path
import SplatStats as splat
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


(iPath, oPath) = (
    path.expanduser('~/Documents/GitHub/s3s/'),
    path.expanduser('~/Documents/Sync/BattlesData/')
)
###############################################################################
# Create Player Objects
###############################################################################
# historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
battles = splat.loadBattlesFromFiles(bPaths)
splat.getPlayerCountsInBattles(battles)



###############################################################################
# Create Player Objects
###############################################################################
chip = splat.Player('čħîþ ウナギ', bPaths, id=7293)
# yami =   splat.Player('Yami ウナギ', bPaths, id=None)
# april =  splat.Player('April ウナギ', bPaths, id=None)
# richie = splat.Player('Riché ウナギ', bPaths, id=None)
# memo =   splat.Player('Oswal　ウナギ', bPaths, id=None)
# tomas =  splat.Player('Murazee', bPaths, id=None)
# Group players for iterations ------------------------------------------------
# team = (chip, yami, april, richie, memo, tomas)


chip.getAlliesAndEnemiesCounts()

chip.battleRecords[1].datetime
chip.battleRecords[1].matchMode
chip.battleRecords[1].festMatch

chip.battlesHistory

bPaths


bDetails = chip.battleRecords
bDetail = chip.battleRecords[0]
bDetail

(allies, enemies) = ([], [])
for bDetail in bDetails:
    pDict = bDetail.getAlliesAndEnemiesNames()
    allies.append(pDict['allies'])
    enemies.append(pDict['enemies'])
(allies, enemies) = [splat.flattenList(i) for i in (allies, enemies)] 
(alliesC, enemiesC) = [Counter(i) for i in (allies, enemies)]


bDetail.getAlliesAndEnemies()


###############################################################################
# Player ranking
###############################################################################
df = chip.getPlayerFullRanking()
dct = Counter(df['kill'])
sorted(dct.items(), key=lambda x: x[1])[::-1]
cats = ['kill', 'death', 'assist', 'special', 'paint']
pd.DataFrame.from_dict({
    i: df[i].value_counts() for i in cats
})


dfA = df.drop('datetime', axis=1)
sns.countplot(dfA.melt(value_vars=dfA.columns), x='value', hue='variable')

(fig, ax) = plt.subplots()
df['kill'].value_counts().plot(ax=ax, kind='bar')
df['death'].value_counts().plot(ax=ax, kind='bar')
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
fName = hFiles[-1]
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
battle.datetime
battle.festMatch
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