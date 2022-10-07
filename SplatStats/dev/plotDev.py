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
plyr = splat.Player(NAMES[3], bPaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
###############################################################################
#  Waffle Dev
###############################################################################
bHist = playerHistory
PLUS = 10
nEntry = bHist.shape[0]
(RMIN, RMAX) = (0, 30)
(PMIN, PMAX) = (0, 2000)
(ANGLES, BOTTOM, TOP, PAINT) = (
    np.linspace(0, 2*np.pi, bHist.shape[0], endpoint=False),
    np.array(bHist['death']),
    np.array(bHist['kill']),
    np.array(bHist['paint'])
)
PAINT = np.array([np.interp(i, (PMIN, PMAX), (RMIN, RMAX)) for i in PAINT])

CLRS = [
    splat.CLR_STATS['kill'] if i>=0 else splat.CLR_STATS['death'] 
    for i in (TOP-BOTTOM)
]
(fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
ax.set_theta_offset(np.pi/2)
ax.vlines(ANGLES, PLUS, PLUS+PAINT,  lw=1, colors=splat.CLR_PAINT, alpha=.1)
ax.vlines(ANGLES, PLUS+BOTTOM, PLUS+TOP, lw=0.5, colors=CLRS, alpha=.7)
ax.set_yticks(np.arange(RMIN+PLUS, RMAX+PLUS, 10))
ax.set_yticklabels([])
xlab = [bHist['datetime'].iloc[int(dt)] for dt in np.arange(0,nEntry, nEntry/10)]
ax.set_xticks([])
# ax.set_xticks(np.arange(0, 2*np.pi, 2*np.pi/10), lw=0)
# ax.set_xticklabels([f"{i.day:02d}/{i.month:02d}" for i in xlab])
ax.set_ylim(RMIN, RMAX+PLUS)
fig.savefig(
    path.join(oPath, (plyr.name)+' Iris.png'), 
    dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor()
)


###############################################################################
# Windowed average
###############################################################################
playerHistory['matches'] = [1]*playerHistory.shape[0]
playerHistory['win bool'] = np.asarray([i=='W' for i in playerHistory['win']])

dailyHistory = playerHistory.groupby(
    playerHistory['datetime'].dt.floor('h')
).sum()
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
df = splat.calcStatsByKey(playerHistory, 'main weapon')
(fig, ax) = plt.subplots(figsize=(5, 5))
splat.plotTreemapByKey(
    (fig, ax), df, 
    'main weapon', metric='kill ratio',
    alpha=0.6
)
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

