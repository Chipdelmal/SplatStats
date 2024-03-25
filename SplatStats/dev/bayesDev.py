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
#     'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'April ウナギ', 'Rei ウナギ',
#     'Oswal　ウナギ', 'Murazee'
###############################################################################
ally = 'Riché ウナギ'
# Wins with ally --------------------------------------------------------------
fltr = (df['win']==True, df[ally]==True)
bools = [all(i) for i in zip(*fltr)]
wins_w_ally = df[bools].shape[0]
# Wins without ally -----------------------------------------------------------
fltr = (df['win']==True, df[ally]==False)
bools = [all(i) for i in zip(*fltr)]
win_n_ally = df[bools]
# Matches counts --------------------------------------------------------------
wins = df[df['win']==True].shape[0]
allyMatches = df[df[ally]==True].shape[0]
totals = df.shape[0]
# Elements --------------------------------------------------------------------
(pa, pw, paw) = (
    allyMatches/totals, 
    wins/totals,
    wins_w_ally/wins
)
bayes = (paw*pw)/pa
# Wins with ally --------------------------------------------------------------
f'{PLYR} with {ally}: {bayes/pw:.4f} ({bayes:.4f}/{pw:.4f})'
###############################################################################
# Return dataframe
###############################################################################
df['main weapon'].unique()
ally = 'Splattershot Jr.'
# Wins with ally --------------------------------------------------------------
fltr = (df['win']==True, df['main weapon']==ally)
bools = [all(i) for i in zip(*fltr)]
wins_w_ally = df[bools].shape[0]
# Wins without ally -----------------------------------------------------------
fltr = (df['win']==True, df['main weapon']!=ally)
bools = [all(i) for i in zip(*fltr)]
win_n_ally = df[bools]
# Matches counts --------------------------------------------------------------
wins = df[df['win']==True].shape[0]
allyMatches = df[df['main weapon']==ally].shape[0]
totals = df.shape[0]
# Elements --------------------------------------------------------------------
(pa, pw, paw) = (
    allyMatches/totals, 
    wins/totals,
    wins_w_ally/wins
)
bayes = (paw*pw)/pa
# Wins with ally --------------------------------------------------------------
print(f'{PLYR} with {ally}: {bayes/pw:.4f} ({bayes:.4f}/{pw:.4f})')
###############################################################################
# Return dataframe
###############################################################################
(MIN_MATCHES, dWpn) = (25, {})
aWpns = df['main weapon'].unique()
nWpns = len(aWpns)
for ally in aWpns:
    nMatches = df[df['main weapon']==ally].shape[0]
    if (nMatches<MIN_MATCHES):
        continue
    # Wins with ally ----------------------------------------------------------
    fltr = (df['win']==True, df['main weapon']==ally)
    bools = [all(i) for i in zip(*fltr)]
    wins_w_ally = df[bools].shape[0]
    # Wins without ally -------------------------------------------------------
    fltr = (df['win']==True, df['main weapon']!=ally)
    bools = [all(i) for i in zip(*fltr)]
    win_n_ally = df[bools]
    # Matches counts ----------------------------------------------------------
    wins = df[df['win']==True].shape[0]
    allyMatches = df[df['main weapon']==ally].shape[0]
    totals = df.shape[0]
    # Elements ----------------------------------------------------------------
    (pa, pw, paw) = (
        allyMatches/totals, 
        wins/totals,
        wins_w_ally/wins
    )
    bayes = (paw*pw)/pa
    # Wins with ally ----------------------------------------------------------
    print(f'{PLYR} with {ally}: {bayes/pw:.4f} ({bayes:.4f}/{pw:.4f})')
    dWpn[ally] = bayes
dWpn