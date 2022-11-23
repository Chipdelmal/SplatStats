#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import markers
from collections import Counter

if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s_source/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Create Player Objects
###############################################################################
# historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 'DantoNnoob'
)
plyr = splat.Player(NAMES[1], bPaths, timezone='America/Los_Angeles')
# (chip, yami, april, richie, memo, tomas) = [
#     splat.Player(nme, bPaths, timezone='America/Los_Angeles')
#     for nme in NAMES
# ]
# team = (chip, yami, april, richie, memo, tomas)
###############################################################################
# Fixing Rank counts
###############################################################################
cats=['kill', 'death', 'assist', 'special', 'paint']

battlesHistory = plyr.battlesHistory
btlRecords = plyr.battleRecords
name = plyr.name

rnks = []
for btl in btlRecords[:]:
    dfA = btl.getAlliedRanks(cats=cats)
    dfE = pd.concat(btl.getEnemiesRanks(cats=cats))
    if name in set(dfA['player name']):
        fltr = dfA[dfA['player name'] == name]
        rnks.append(fltr)
    elif name in set(dfE['player name']):
        fltr = dfE[dfE['player name'] == name]
        rnks.append(fltr)
df = pd.concat(rnks, axis=0).drop(columns=['player name', 'player name id'])
# Filter invalid battles and make indexes match -----------------------
bHist = battlesHistory
vIx = list(bHist.index)
df = df.iloc[vIx]
df = df.set_index(pd.Series(vIx))
df['datetime'] = bHist['datetime']

###############################################################################
# Pulling out some stats
###############################################################################
bHist = plyr.battlesHistory
plyr.playerStats



plyr.getAlliesAndEnemiesCounts()['allies']
bFiltered = bHist[bHist['main weapon'] == 'Splattershot']
splat.calcBattleHistoryStats(bFiltered)
plyr.getPlayerHistoryByTypes()