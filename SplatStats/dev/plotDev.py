#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
from math import radians, log10
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
# Streaks
###############################################################################
wins = list(playerHistory['win'])
splat.longestRun(wins, elem='W')
splat.longestRun(wins, elem='L')
###############################################################################
# Windowed average
###############################################################################
kSize = 10
dHist = splat.aggregateStatsByPeriod(playerHistory, period='2H')
winsArray = np.asarray((dHist['win'])/dHist['matches'])
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
#  Circle Barchart
###############################################################################
(cat, stat, aggFun) = ('main weapon', 'kassist', np.mean)
(autoRange, xRange, logScale) = (True, (0, 10), True)
rRange = (0, 270)
gStep = 50

colors = [
    '#C70864', '#C6D314', '#4B25C9', '#830B9C', '#2CB721',
    '#0D37C3', '#C920B7', '#571DB1', '#14BBE7', '#38377A'
]
colors.reverse()
# Gather data -----------------------------------------------------------------
df = playerHistory.groupby(cat).agg(aggFun)
df.sort_values(by=[stat], inplace=True)
catVals = list(df[stat])
# Scaling stats values --------------------------------------------------------
gGrid = np.arange(0, max(catVals), max(catVals)/gStep)
if logScale:
    vVals = [log10(i+1) for i in catVals]
    xRan = (0, max(vVals) if autoRange else xRange[1])
    gVals = [log10(i+1) for i in gGrid]
else:
    vVals = catVals
    xRan = (0, max(vVals) if autoRange else xRange[1])
    gVals = gGrid
weapons = list(df.index)
angles = [np.interp(i, xRan, rRange) for i in vVals]
grids = [np.interp(i, xRan, rRange) for i in gVals]
# Generate Plot ---------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
for (i, ang) in enumerate(angles):
    ax.barh(i, radians(ang), color=colors[i])
ax.vlines(
    [radians(i) for i in grids], len(weapons)-.5, len(weapons),  
    lw=1, colors='k', alpha=.5
)
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.spines['polar'].set_visible(False)
ax.set_theta_zero_location('N')
ax.set_theta_direction(1)
ax.set_rlabel_position(0)
# ax.grid(False)
# ax.set_thetagrids(rRange, [], color='#00000000') # gGrid)
ax.set_xticks([])
ax.set_rgrids(
    [i-.25 for i in range(len(weapons))], 
    labels=[f' {w} ({v:.2f})' for (w, v) in zip(weapons, catVals)]
)