#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
import SplatStats as splat
from pywaffle import Waffle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s/'),
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
    'Oswal　ウナギ', 'April ウナギ', 'Murazee'
)
plyr = splat.Player(NAMES[0], bPaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
###############################################################################
# Windowed average
###############################################################################
playerHistory['matches'] = [1]*playerHistory.shape[0]
playerHistory['win bool'] = np.asarray([i=='W' for i in playerHistory['win']])

dailyHistory = playerHistory.groupby(playerHistory['datetime'].dt.floor('h')).sum()
winsArray = np.asarray(dailyHistory['kill']/dailyHistory['matches'])

kernel_size = 10
kernel = np.ones(kernel_size)/kernel_size
data_convolved = np.convolve(winsArray, kernel, mode='valid')

plt.plot(winsArray)
plt.plot([i+kernel_size/2 for i in range(len(data_convolved))], data_convolved)
###############################################################################
# Stages Treemap
###############################################################################
stagesStatsMatch = splat.calcStagesStatsByType(playerHistory)
stagesDF = splat.calcStagesStats(playerHistory)
stagesDF = stagesStatsMatch['Turf War']

(fig, ax) = plt.subplots(figsize=(5, 5))
(fig, ax) = splat.plotTreemapByStages(
    (fig, ax), stagesDF, metric='kill ratio', 
    fmt='{:.2f}', pad=0.1, alpha=.5
)
fig.savefig(
    path.join(oPath, (plyr.name)+' Treemap.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Dev
###############################################################################
df = splat.calcStatsByKey(
    playerHistory, 
    key='main weapon', sortBy='win ratio', ascending=False
)

alpha = .45
colors = [
    i+splat.alphaToHex(alpha) for i in splat.CLR_CLS_LONG[:len(df['main weapon'])]
]

fig = plt.figure(
    FigureClass=Waffle,
    rows=18, 
    # columns=20,
    values=df['total matches'],
    labels=list(df['main weapon']),
    starting_location='NW',
    vertical=False,
    block_arranging_style='snake',
    colors=colors,
    alpha=.35,
    # labels=[f"{k} ({int(v / sum(data.values()) * 100)}%)" for k, v in data.items()],
    legend={
        'loc': 'upper left',
        'bbox_to_anchor': (1, 1),
        'ncol': 1,
        'framealpha': 0,
        'fontsize': 12
    }
)
plt.title('total matches')




xInter = np.interp(1, (0, 1), (0, 255))
hex(round(xInter))[2:]

def alphaToHex(alphaFloat):
    xInter = np.interp(alphaFloat, (0, 1), (0, 255))
    xHex = hex(round(xInter))
    return xHex[2:]