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
from matplotlib import font_manager
font_dirs = ['/home/chipdelmal/Documents/Sync/BattlesData/']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)
plt.rcParams["font.family"]="Splatfont 2"


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
(fig, ax) = splat.plotCircularBarchartStat(
    playerHistory, cat='main weapon', stat='kassist', aggFun=np.sum,
    colors=wColors, yRange=(0, 10), ticksStep=5, logScale=False,
    ticksFmt={
        'lw': 1, 'range': (-0.5, -0.25), 
        'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.2f}'
    }
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

fpath = Path(mpl.get_data_path(), "fonts/ttf/cmr10.ttf")

plt.rcParams['font.sans-serif'] = 'Splatfont2'

splat.polarBarChart(['Splatoon', 'b', 'c'], [1, 0.5, .2])