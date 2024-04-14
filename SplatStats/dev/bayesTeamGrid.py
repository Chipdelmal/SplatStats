#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from os import path
import SplatStats as splat
import matplotlib.pyplot as plt


(TEAM, STATS, BATS) = (
    [ 
        'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'April ウナギ', 'Rei ウナギ',
        'Oswal　ウナギ', 'Murazee'
    ],
    (
        'main weapon', 'sub weapon', 'special weapon', 
        'win', 'kill', 'death', 'assist', 'paint', 'special'
    ),
    ('ko', 'matchType', 'duration', 'stage', 'festMatch')
)
(iPath, bPath, oPath) = (
    path.expanduser('~/Documents/BattlesDocker/jsons'),
    path.expanduser('~/Documents/BattlesDocker/battles'),
    path.expanduser('~/Documents/BattlesDocker/out')
)
###############################################################################
# Setup Splats Font
###############################################################################
fontPath = path.expanduser('~/Documents/BattlesDocker/')
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Iterate over players
###############################################################################
tLen = len(TEAM)
(pMat, mMat) = (np.zeros((tLen, tLen))), np.zeros((tLen, tLen))
PLYR = TEAM[0]
# Load current player's stats ---------------------------------------------
plyr = splat.Player(PLYR, bFilepaths, timezone='America/Los_Angeles')
btlsDF = splat.getAlliesEnemiesDataFrames(plyr.battleRecords, PLYR, TEAM)
(dfA, dfE) = (btlsDF['allies'], btlsDF['enemies'])
###########################################################################
# Bayes
###########################################################################
grid = np.arange(0, 21.5, 0.5)
(tLen, rLen) = (len(TEAM), grid.shape[0])
(pMat, mMat) = (np.zeros((rLen, tLen))), np.zeros((rLen, tLen))
for (r, ths) in enumerate(grid):
    for (c, ALLY) in enumerate(TEAM):
        cond = (
            ((dfA['kill']+dfA['assist']*0.5)<=ths*dfA['death']) 
            # (dfA['win']==True)
        )
        (wins, matches) = (
            dfA.loc[(cond)].shape[0],
            dfA.shape[0]    
        )
        like = dfA.loc[(dfA[ALLY] & cond)].shape[0]
        (likelihood, prior, marginal) = (
            (like/wins if wins>0 else 0),
            dfA.loc[(cond)].shape[0]/matches,
            dfA.loc[(dfA[ALLY])].shape[0]/matches
        )
        bayes = (likelihood*prior)/marginal # (0 if (marginal==0) else )
        pMat[r,c] = bayes
        mMat[r,c] = dfA.loc[(dfA[ALLY])].shape[0]     
###############################################################################
# Plot Matrix
###############################################################################
cList = [
    '#C1D0F9', '#D6F6F6', '#A9A7BC', '#FEF0FB', 
    '#FEDEF7', '#E1CCEE', '#E6AFC3', '#FFCC9C'
]
cmap = splat.colorPaletteFromHexList(cList)
(fig, ax) = plt.subplots(figsize=(10, 10))
for (ix, row) in enumerate(pMat.T):
    ax.plot(range(rLen), row, color=cList[ix], lw=3, alpha=0.7)
    # ax.scatter(range(rLen), row, color=cList[ix], alpha=0.75, zorder=1)
xLen = np.arange(0, int(max(grid)), 1).shape[0]
ax.set_xticks(
    np.arange(0, rLen, rLen/xLen), 
    [int(i) for i in np.arange(0, max(grid), 1)]
)
ax.set_ylabel("P(Event | Ally)", fontsize=20)
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.set_xlim(0, rLen-2)
ax.set_ylim(0, 1)
ax.legend(TEAM)
ax.grid(True)
# ax.set_facecolor("#000000")
# plt.figure(facecolor="#000000")
# fig.patch.set_facecolor("#000000")


