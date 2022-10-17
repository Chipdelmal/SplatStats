#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sys import argv
from os import path
import SplatStats as splat
from scipy import stats
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
from SplatStats.Player import Player
from SplatStats.constants import MKR_STATS


def gaussian_smooth(x, y, grid, sd):
    weights = np.transpose([stats.norm.pdf(grid, m, sd) for m in x])
    weights = weights / weights.sum(0)
    return (weights * y).sum(1)


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Create Player Objects
##############################################################################
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'Oswal　ウナギ', 
    'April ウナギ', 'Rei ウナギ', 'DantoNnoob'# , 'Murazee'
)
tz = 'America/Los_Angeles'
plyrs = {name: splat.Player(name, bPaths, timezone=tz) for name in NAMES}
###############################################################################
# Initial Tests
###############################################################################
df = pd.concat([plyrs[nme].battlesHistory for nme in NAMES], axis=0)
playerHistory = df # plyrs[NAMES[0]].battlesHistory
playerHistory['matches'] = [1]*playerHistory.shape[0]
playerHistory['win bool'] = np.asarray([i=='W' for i in playerHistory['win']])
dailyHistory = playerHistory.groupby(
    playerHistory['datetime'].dt.floor('h')
).sum()
dailyHistory.sum()
# Date-sorted -----------------------------------------------------------------
datesSet = [set(plyrs[nme].battlesHistory['datetime']) for nme in NAMES]
dates = sorted(list(set.union(*datesSet)))
###############################################################################
# Streamchart
###############################################################################
df = pd.concat([plyrs[nme].battlesHistory for nme in NAMES], axis=0)
dfs = []
for nme in NAMES:
    dfTemp = plyrs[nme].battlesHistory
    dfTemp['player'] = [nme]*(dfTemp.shape[0])
    dfTemp['matches'] = [1]*(dfTemp.shape[0])
    dfs.append(dfTemp)
dfTeam = pd.concat(dfs, axis=0)
# Grouping --------------------------------------------------------------------
cats = ['kill', 'death', 'assist', 'special', 'paint', 'matches']
catsDF = ['player', 'datetime'] + cats
dfGrp = dfTeam[catsDF].groupby(['datetime', 'player']).sum()
(dates, names) = (
    sorted(list(df['datetime'].unique())),
    list(dfTeam['player'].unique())
)
dfPadded = dfGrp.unstack(fill_value=0).stack()
# Generate series -------------------------------------------------------------
dfByHour = dfPadded.unstack().resample('H').sum().stack()
dfByPlayer = dfByHour.reorder_levels(["player", "datetime"])
# Final array -----------------------------------------------------------------
entryNum = dfByPlayer.loc[names[0]].shape[0]
stream = np.zeros((len(names), entryNum))
for (ix, name) in enumerate(names):
    stream[ix]  = np.array(dfByPlayer.loc[name]['kill'])
# Plot ------------------------------------------------------------------------
streamFiltered = stream[:,np.any(stream > 0, axis=0)]
cSum = np.sum(streamFiltered, axis=0)
streamNormalized = np.array([r/cSum for r in streamFiltered])

x = range(streamFiltered.shape[1])

grid = np.linspace(0, streamFiltered.shape[1], num=500)
y_smoothed = [gaussian_smooth(x, y_, grid, 1) for y_ in streamFiltered]


COLORS = [
    "#0D40DE", "#EC0B68", "#6ABF0B", "#9090BA",
    "#A577FF", "#A6BDDB", "#E4E567", "#CFD1C7"
]

fig, ax = plt.subplots(figsize=(10, 7))
ax.stackplot(grid, y_smoothed, baseline="zero", colors=COLORS)
ax.set_xlim(0, max(x))
# ax.set_ylim(0, 5)
# ax.legend(names)


fig, ax = plt.subplots(figsize=(10, 7))
ax.stackplot(x, streamFiltered, baseline="zero", colors=COLORS)
ax.set_xlim(0, max(x))
# ax.set_ylim(0, 1)


