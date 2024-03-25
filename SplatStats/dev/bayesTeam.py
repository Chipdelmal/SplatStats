#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from os import path
import bambi as bmb
from collections import Counter
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
PLYR = TEAM[0]
# Load current player's stats -------------------------------------------------
plyr = splat.Player(PLYR, bFilepaths, timezone='America/Los_Angeles')
btlsDF = splat.getAlliesEnemiesDataFrames(plyr.battleRecords, PLYR, TEAM)
(dfA, dfB) = (btlsDF['allies'], btlsDF['enemies'])
###############################################################################
# Bayes
###############################################################################
ally = TEAM[6]

matches = dfA.shape[0]
(likelihood, prior, marginal) = (
    dfA.loc[(dfA[ally] & dfA['win'])].shape[0]/dfA.loc[(dfA['win'])].shape[0],
    dfA.loc[(dfA['win'])].shape[0]/matches,
    dfA.loc[(dfA[ally])].shape[0]/matches
)
bayes = (likelihood*prior)/marginal
bayes

