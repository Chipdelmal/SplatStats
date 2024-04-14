#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from os import path
import matplotlib.pyplot as plt
import SplatStats as splat



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
for (r, PLYR) in enumerate(TEAM):
    # Load current player's stats ---------------------------------------------
    plyr = splat.Player(PLYR, bFilepaths, timezone='America/Los_Angeles')
    btlsDF = splat.getAlliesEnemiesDataFrames(plyr.battleRecords, PLYR, TEAM)
    (dfA, dfE) = (btlsDF['allies'], btlsDF['enemies'])
    ###########################################################################
    # Bayes
    ###########################################################################
    ALLY = TEAM[0]
    for (c, ALLY) in enumerate(TEAM):
        cond = (
            (dfA['kill'] < dfA['death'])
        )
        (wins, matches) = (
            dfA.loc[(cond)].shape[0],
            dfA.shape[0]    
        )
        like = dfA.loc[(dfA[ALLY] & cond)].shape[0]
        (likelihood, prior, marginal) = (
            (like/wins if like>0 else 0),
            dfA.loc[(cond)].shape[0]/matches,
            dfA.loc[(dfA[ALLY])].shape[0]/matches
        )
        bayes = (0 if (marginal==0) else (likelihood*prior)/marginal)
        pMat[r,c] = bayes
        mMat[r,c] = dfA.loc[(dfA[ALLY])].shape[0]
###############################################################################
# Plot Matrix
###############################################################################
(ctr, delta, cList) = (
    0, 0.5, 
    ['#E84E73', '#f8f7ff', '#f8f7ff', '#9381ff']
)
cmap = splat.colorPaletteFromHexList(cList)
(fig, ax) = plt.subplots(figsize=(6, 6))
ax.matshow(pMat, cmap=cmap, vmin=ctr-delta, vmax=ctr+delta)
for (i, j), z in np.ndenumerate(pMat):
    ax.text(
        j, i, 
        '{:0.2f}\n({:0.0f})'.format(z, mMat[j, i]), 
        ha='center', va='center', fontsize=9
    )
ax.set_xticklabels(['']+TEAM, rotation=90)
ax.set_yticklabels(['']+TEAM)