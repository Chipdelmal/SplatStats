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

from SplatStats.plots import plotKillsAndDeathsHistogram
# plt.rcParams["font.family"]="Roboto Mono"

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
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'DantoNnoob',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 'Rei ウナギ'
)
plyr = splat.Player(NAMES[0], bPaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
###############################################################################
# Windowed average
###############################################################################
playerHistory['matches'] = [1]*playerHistory.shape[0]
playerHistory['win bool'] = np.asarray([i=='W' for i in playerHistory['win']])

dailyHistory = playerHistory.groupby(
    playerHistory['datetime'].dt.floor('h')
).sum()
winsArray = np.asarray((dailyHistory['kill']+.5*dailyHistory['assist'])/dailyHistory['matches'])

kernel_size = 10
kernel = np.ones(kernel_size)/kernel_size
data_convolved = np.convolve(winsArray, kernel, mode='valid')

(fig, ax) = plt.subplots(figsize=(10, 4))
ax.plot(winsArray, lw=5, color=splat.LUMIGREEN_V_DFUCHSIA_S1[-1], alpha=.25)
ax.plot(
    [i+kernel_size/2 for i in range(len(data_convolved))], data_convolved,
    lw=2.5, color=splat.PINK_V_GREEN_S1[0], alpha=.85
)
ax.autoscale(enable=True, axis='x', tight=True)
ax.set_ylim(0, 25)
###############################################################################
# Stages Treemap
###############################################################################
stagesStatsMatch = splat.calcStagesStatsByType(playerHistory)
stagesDF = splat.calcStagesStats(playerHistory)
stagesDF = stagesStatsMatch['Splat Zones']

(fig, ax) = plt.subplots(figsize=(5, 5))
(fig, ax) = splat.plotTreemapByStages(
    (fig, ax), stagesDF, metric='win ratio', 
    fmt='{:.2f}', pad=0.1, alpha=.5
)
fig.savefig(
    path.join(oPath, (plyr.name)+' Treemap.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Dev
###############################################################################
(dfKey, metric) = ('sub weapon', 'kills avg')
df = splat.calcStatsByKey(playerHistory, dfKey)
(fig, ax) = plt.subplots(figsize=(5, 5))
splat.plotTreemapByKey((fig, ax), df, dfKey, metric=metric, alpha=0.75)
###############################################################################
#  Waffle Dev
###############################################################################
alpha = .45
colors = [
    i+splat.alphaToHex(alpha) for i in splat.CLR_CLS_LONG[:len(df['main weapon'])]
]
(fig, ax) = plt.subplots(figsize=(15, 7.5))
ax.set_aspect(aspect="equal")
Waffle.make_waffle(
    ax=ax,
    rows=25, 
    # columns=50,
    values=df['kills'],
    labels=list(df['main weapon']),
    starting_location='NW',
    vertical=False,
    block_arranging_style='snake',
    colors=colors,
    interval_ratio_x=.5,
    interval_ratio_y=.5,
    # labels=[f"{k} ({int(v / sum(data.values()) * 100)}%)" for k, v in data.items()],
    legend={
        'loc': 'lower left',
        'bbox_to_anchor': (0, -.5),
        'ncol': 5,
        'framealpha': 0,
        'fontsize': 12
    }
)
plt.title('kills')
fig.savefig(
    path.join(oPath, (plyr.name)+' Waffle.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)

