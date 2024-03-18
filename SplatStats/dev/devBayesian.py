#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from os import path
import bambi as bmb
from collections import Counter
import SplatStats as splat


(PLYR, MATES, STATS, BATS) = (
    'čħîþ ウナギ',
    [ 
        'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'April ウナギ', 'Rei ウナギ',
        'Oswal　ウナギ', 'Murazee'
    ],
    ('win', 'kill', 'death', 'assist', 'paint', 'special'),
    ('ko', 'matchType', 'duration', 'stage', 'festMatch')
)
(iPath, bPath, oPath) = (
    path.expanduser('~/Documents/BattlesDocker/jsons'),
    path.expanduser('~/Documents/BattlesDocker/battles'),
    path.expanduser('~/Documents/BattlesDocker/out')
)
fontPath = path.expanduser('~/Documents/BattlesDocker/')
###############################################################################
# Setup Splats Font
###############################################################################
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=False)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Load Player Data
###############################################################################
plyr = splat.Player(PLYR, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
phLen = playerHistory.shape[0]
MATES.remove(PLYR)
###############################################################################
# Examine battles
###############################################################################
ix = 0
nBattles = len(plyr.battleRecords)
bList = []
for ix in range(nBattles):
    bRecord = plyr.battleRecords[ix]
    (allies, enemies) = (bRecord.alliedTeam, bRecord.enemyTeams)
    if PLYR not in set(allies['player name']):
        continue
    # Get battle stats --------------------------------------------------------
    bttlStats = {s: bRecord.__getattribute__(s) for s in BATS}
    # Get player row and outcome ----------------------------------------------
    plyrEntry = allies[allies['player name']==PLYR]
    plyrStats = {s: plyrEntry[s].values[0] for s in STATS}
    # Get if allies are present -----------------------------------------------
    allyPrsnt = {n: (n in set(allies['player name'])) for n in MATES}
    # Assemble full dictionary ------------------------------------------------
    bDicts = [bttlStats, plyrStats, allyPrsnt]
    bList.append({k: v for d in bDicts for k, v in d.items()})
# Generate dataframe and clean ------------------------------------------------
df = pd.DataFrame.from_dict(bList)
df = df[df['win']!='NA']
df['win'] = df['win'].map({'W': 1, 'L': 0})
###############################################################################
# Return dataframe
###############################################################################
df