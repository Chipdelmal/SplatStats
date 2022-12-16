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
cats = ['kill', 'death', 'assist', 'paint']
dfRank = plyr.getPlayerFullRanking(cats=cats)

splat.polarBarRanks(dfRank, 8)


cats = ['kill', 'death', 'assist', 'paint']
dfRank = plyr.getPlayerFullRanking(cats=cats)
vals = {}
for cat in cats:
    vals[cat] = list(dfRank[cat].value_counts(sort=False, normalize=True).sort_index())[::-1]


yRange = (0, 1)
ranksNum = 8
thetaRange = (0, 90)
colors=['#EC0B68', '#3D59DE', '#6BFF00', '#38377A']

fig = plt.figure(figsize=(10, 10))
gs = fig.add_gridspec(
    2, 2,  
    width_ratios=(1, 1), height_ratios=(1, 1),
    left=0.1, right=0.9, bottom=0.1, top=0.9,
    wspace=0.075, hspace=0.075
)
ax_k = fig.add_subplot(gs[0], projection='polar')
ax_d = fig.add_subplot(gs[1], sharex=ax_k, projection='polar')
ax_a = fig.add_subplot(gs[2], sharey=ax_d, projection='polar')
ax_p = fig.add_subplot(gs[3], sharex=ax_a, projection='polar')
# Plot Sectors ------------------------------------------------------------
(fig, ax_k) = splat.polarBarChart(
    range(1, ranksNum+1)[::-1], vals[cats[0]], figAx=(fig, ax_k),
    logScale=False, rRange=(0, 90), yRange=yRange, labels=True,
    origin='W', direction=-1, colors=[colors[0]]*ranksNum
)
ax_k.set_thetamin(thetaRange[0]); ax_k.set_thetamax(thetaRange[1])
ax_k.text(.25, .9, cats[0], fontsize=15, ha='right', transform=ax_k.transAxes)
[x.set_linewidth(1.5) for x in ax_k.spines.values()]
# ax.set(frame_on=False)
(fig, ax_d) = splat.polarBarChart(
    range(1, ranksNum+1)[::-1], vals[cats[1]], figAx=(fig, ax_d),
    logScale=False, rRange=(0, 90), yRange=yRange, labels=True,
    origin='N', direction=-1, colors=[colors[1]]*ranksNum
)
ax_d.set_thetamin(thetaRange[0]); ax_d.set_thetamax(thetaRange[1])
ax_d.text(.75, .9, cats[1], fontsize=15, ha='left', transform=ax_d.transAxes)
[x.set_linewidth(1.5) for x in ax_d.spines.values()]
# ax.set(frame_on=False)
(fig, ax_a) = splat.polarBarChart(
    range(1, ranksNum+1)[::-1], vals[cats[2]], figAx=(fig, ax_a),
    logScale=False, rRange=(0, 90), yRange=yRange, labels=True,
    origin='S', direction=-1, colors=[colors[2]]*ranksNum
)
ax_a.set_thetamin(thetaRange[0]); ax_a.set_thetamax(thetaRange[1])
ax_a.text(.25, .1, cats[3], fontsize=15, ha='right', transform=ax_a.transAxes)
[x.set_linewidth(1.5) for x in ax_a.spines.values()]
# ax.set(frame_on=False)
(fig, ax_p) = splat.polarBarChart(
    range(1, ranksNum+1)[::-1], vals[cats[3]], figAx=(fig, ax_p),
    logScale=False, rRange=(0, 90), yRange=yRange, labels=True,
    origin='E', direction=-1, colors=[colors[3]]*ranksNum
)
ax_p.set_thetamin(thetaRange[0]); ax_p.set_thetamax(thetaRange[1])
ax_p.text(.75, .1, cats[2], fontsize=15, ha='left', transform=ax_p.transAxes)
[x.set_linewidth(1.5) for x in ax_p.spines.values()]