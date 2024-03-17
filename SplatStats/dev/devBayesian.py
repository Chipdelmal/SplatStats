#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sys import argv
from os import path
from collections import Counter
import SplatStats as splat
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


(PLYR, MATES, STATS) = (
    'čħîþ ウナギ',
    ( 
        'Yami ウナギ', 'Riché ウナギ', 'April ウナギ', 'Rei ウナギ',
        'Oswal　ウナギ', 'Murazee'
    ),
    ('win', 'kill', 'death', 'assist', 'paint', 'special')
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
###############################################################################
# Examine battles
###############################################################################
ix = 1
(allies, enemies) = (
    plyr.battleRecords[ix].alliedTeam,
    plyr.battleRecords[ix].enemyTeams
)
# Get player row and outcome --------------------------------------------------
plyrEntry = allies[allies['player name']==PLYR]
plyrStats = {s: plyrEntry[s].values[0] for s in STATS}

