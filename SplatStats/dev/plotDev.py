#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
from collections import Counter
import SplatStats as splat
from pywaffle import Waffle
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import Normalize
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
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
# Dev
###############################################################################
(dfKey, metric) = ('stage', 'win ratio')
df = splat.calcStagesStatsByType(playerHistory)

(gModes, yRange) = (5, (0, 1))
cDict = splat.CLR_STAGE

(fig, ax) = (plt.figure(figsize=(30, 30)), [None]*gModes)
gs = fig.add_gridspec(
    gModes, 1,  
    width_ratios=(1, ), height_ratios=[1/gModes]*gModes,
    left=0.1, right=0.9, bottom=0.1, top=0.9,
    wspace=0.05, hspace=0
)

dfAmmend = []
cats = ('Tower Control', 'Rainmaker', 'Splat Zones', 'Clam Blitz', 'Turf War')
for cat in cats:
    dfIn = df[cat]
    # Amend for same stages shape ---------------------------------------------
    (stgs, allStages) = (list(dfIn[dfKey]), list(cDict.keys()))
    for stg in list(cDict.keys()):
        if not (stg in set(allStages)):
            print(1)
            dfIn.loc[len(dfIn)] = [stg]+[0]*(dfIn.shape[1]-1)
    dfIn.sort_values(dfKey, inplace=True)
    # Add match type ----------------------------------------------------------
    dfIn['match type'] = [cat]*dfIn.shape[0]
    dfAmmend.append(dfIn)
dfOut = pd.concat(dfAmmend)

g = sns.FacetGrid(dfOut, row="match type", aspect=4)
g.map(sns.barplot, metric, dfKey, palette=[cDict[k] for k in allStages])
g.figure.subplots_adjust(wspace=.02, hspace=.5)


ax[0] = fig.add_subplot(gs[0])
ax[0].set_xticks([])
ax[0].set_yticks([])
sns.barplot(
    ax=ax[0], 
    data=dfIn, x=metric, y=dfKey,
    capsize=.4, errcolor=".5",
    linewidth=0, edgecolor=".5", 
    palette=[cDict[k] for k in allStages]
)

fig

###############################################################################
# Windowed average
###############################################################################
kSize = 10
dHist = splat.aggregateStatsByPeriod(playerHistory, period='1H')
winsArray = np.asarray((dHist['kassist'])/dHist['matches'])
windowAvg = splat.windowAverage(winsArray, kernelSize=kSize, mode='valid')

(fig, ax) = plt.subplots(figsize=(10, 4))
ax.plot(winsArray, lw=5, color=splat.LUMIGREEN_V_DFUCHSIA_S1[-1], alpha=.15)
ax.plot(
    [i+kSize/2 for i in range(len(windowAvg))], windowAvg,
    lw=4, color=splat.PINK_V_GREEN_S1[0], alpha=.85
)
ax.autoscale(enable=True, axis='x', tight=True)
ax.set_ylim(0, max(winsArray))
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

