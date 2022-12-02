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
# Circle Barchart
###############################################################################
wColors = [
    '#2DD9B6', '#4F55ED', '#B14A8D', '#7F7F99', '#990F2B',
    '#C70864', '#C6D314', '#4B25C9', '#830B9C', '#2CB721',
    '#0D37C3', '#C920B7', '#571DB1', '#14BBE7', '#38377A'
][::-1]
(fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
(fig, ax) = splat.plotCircularBarchartStat(
    (fig, ax),
    playerHistory, 'main weapon', 'kassist', np.sum,
    colors=wColors
)
###############################################################################
# Divide BarChart
###############################################################################
cat = 'main weapon'
aggFun = np.sum
stat = 'kassist'
# Gather data -------------------------------------------------------------
df = playerHistory.groupby(cat).agg(aggFun)
df.sort_values(by=[stat], inplace=True)
catVals = list(df[stat])

wColors = [
    '#2DD9B6', '#4F55ED', '#B14A8D', '#7F7F99', '#C70864', 
    '#C6D314', '#4B25C9', '#830B9C', '#2CB721', '#0D37C3', 
    '#C920B7', '#571DB1', '#14BBE7', '#38377A', '#990F2B'
][::-1]

xVals = list(df.index)
yVals = catVals

logScale=True
gStep=10
rRange=(0, 270)
yRange=(0, 10e3)
colors=wColors
labels=True
fmt='{:.0f}' #'{:.2f}'

figAx = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})

(fig, ax) = figAx
# Get value ranges ------------------------------------------------------------
(minValY, maxValY) = [
    0 if not yRange else yRange[0],
    max(yVals) if not yRange else yRange[1]
]
if not yRange:
    yRange = (minValY, maxValY)
# Define grid -----------------------------------------------------------------
stepSizeY = maxValY/gStep
gridY = np.arange(minValY, maxValY+maxValY/stepSizeY, stepSizeY)
# Log-scale if needed ---------------------------------------------------------
if logScale:
    (gridYSca, yValsSca, yRangeSca) =  [
        [log10(i+1) for i in j] for j in (gridY, yVals, yRange)
    ]
else:
    (gridYSca, yValsSca, yRangeSca) =  (gridY, yVals, yRange)
# Convert heights into radii --------------------------------------------------
angleHeights = [np.interp(i, yRangeSca, rRange) for i in yValsSca]
grids = [np.interp(i, yRangeSca, rRange) for i in gridYSca]
# Generate Plot ---------------------------------------------------------------
for (i, ang) in enumerate(angleHeights):
    ax.barh(i, radians(ang), color=colors[i])
# Gridlines and axes ----------------------------------------------------------
ax.vlines(
    [radians(i) for i in grids], len(xVals)-.5, len(xVals)-.25,  
    lw=1, colors='k', alpha=.5
)
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_ylim(-.5, len(yVals)-0.1)
ax.spines['polar'].set_visible(False)
ax.set_theta_zero_location('N')
ax.set_theta_direction(1)
ax.set_rlabel_position(0)
# Labels ----------------------------------------------------------------------
labelsText = [fmt.format(i) for i in gridY] if labels else []
ax.set_thetagrids(grids, labelsText, color='#000000FF')
# Categories Markers ----------------------------------------------------------
ax.set_rgrids(
    [i for i in range(len(xVals))], 
    labels=[f' {w} ({v:.2f})' for (w, v) in zip(xVals, yVals)],
    va='center'
)

