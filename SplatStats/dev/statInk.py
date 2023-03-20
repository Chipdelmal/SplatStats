# !/usr/bin/env python3

from os import path, system
from glob import glob
import numpy as np
import pandas as pd
from random import shuffle
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
import SplatStats as splat


(six, USR) = (0, 'dsk')
SSON = ['Drizzle Season 2022', 'Chill Season 2022', 'Fresh Season 2023']
SEASON = SSON[six]
TOP = 20
###############################################################################
# Get files and set font
###############################################################################
if USR=='lab':
    DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
elif USR=='lap':
    DATA_PATH = '/Users/sanchez.hmsc/Documents/SyncMega/BattlesDocker'
else:
    DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
COLORS = splat.ALL_COLORS
shuffle(COLORS)
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
###############################################################################
# Filter by Constraints
###############################################################################
fltrs = (btls['season']==SEASON, )
fltrBool = [all(i) for i in zip(*fltrs)]
btlsFiltered = btls[fltrBool]
###############################################################################
# Get Total Season Frequencies and Dominance Matrix
###############################################################################
(wpnFreq, wpnWLT, lbyFreq, lbyDaily) = (
    splat.getWeaponsFrequencies(btlsFiltered),
    splat.getWeaponsWLT(btlsFiltered),
    splat.getLobbyFrequencies(btlsFiltered),
    splat.countDailyLobbies(btlsFiltered)
)
lbyGaussDaily = splat.smoothCountDailyLobbies(lbyDaily)
(mNames, mMatrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
(sNames, sMatrix, sSort) = splat.normalizeDominanceMatrix(mNames, mMatrix)
# Calculate auxiliary metrics -------------------------------------------------
wpnRank = splat.rankWeaponsFrequency(wpnFreq, wpnWLT)
(mWpnWins, mWpnLoss) = (
    np.sum(mMatrix, axis=1)/4, 
    np.sum(mMatrix, axis=0)/4
)
# Checks for consistency ------------------------------------------------------
tests = [
    np.sum(list(wpnFreq.values()))/8 == btlsFiltered.shape[0],
    np.sum(list(lbyFreq.values()))   == btlsFiltered.shape[0],
    np.sum(np.sum(wpnWLT[1][:,2]))   == np.sum(list(wpnFreq.values())),
    all(mWpnWins == wpnWLT[1][:,0]),
    all(mWpnLoss == wpnWLT[1][:,1]),
    all(wpnWLT[1][:,2] == mWpnWins+mWpnLoss)
]
assert(all(tests))
###############################################################################
# Lobby Type
###############################################################################
fName = 'Lobby - {}.png'.format(SEASON)
(fig, ax) = plt.subplots(figsize=(0.4, 20))
(fig, ax) = splat.barChartLobby(lbyFreq)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName), dpi=350, 
    transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Plot Total Frequencies
###############################################################################
fName = 'Polar - {}.png'.format(SEASON)
(fig, ax) = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})
(fig, ax) = splat.plotPolarFrequencies(wpnFreq, wpnRank, figAx=(fig, ax))
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###########################################################################
# Weapon Matrix
###########################################################################
fName = 'Matrix - {}.png'.format(SEASON)
COLS = (
    ('#B400FF', '#1D07AC'), 
    ('#D01D79', '#1D07AC'), 
    ('#6BFF00', '#1D07AC')
)
cPal = splat.colorPaletteFromHexList([COLS[six][0], '#FFFFFF', COLS[six][1]])
(fig, ax) = plt.subplots(figsize=(20, 20))
(fig, ax) = splat.plotDominanceMatrix(
    sNames, sMatrix, sSort, mMatrix,
    figAx=(fig, ax), vRange=(-0.75, 0.75), cmap=cPal
)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Gaussian Lobby
###############################################################################
gModes = list(lbyDaily.columns)
gModesCols = ['#DE0B64FF', '#FDFF00FF', '#0D37C3FF', '#71DA0CFF', '#531BBAFF']
(fig, ax) = (plt.figure(figsize=(20, 3)), plt.axes())
ax.stackplot(
    lbyGaussDaily[0][0], *[-y[1] for y in lbyGaussDaily], 
    labels=gModes, baseline='zero',
    colors=gModesCols
)
ax.legend(loc='upper left').remove()
ax.set_xlim(0, lbyGaussDaily[0][0][-1])
ax.set_ylim(0, -1250)
xtickRan = np.arange(0, lbyGaussDaily[0][0][-1], 15)
ax.set_ylim(ax.get_ylim()[::-1])
ax.xaxis.tick_top()
ax.set_xticks(
    xtickRan, 
    ['{}/{}'.format(lbyDaily.index[i].month, lbyDaily.index[i].day) for i in xtickRan],
    ha='left', va='bottom', rotation=0, fontsize=12.5
)
ax.set_yticks([], [])
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
fName = 'Stacked - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')