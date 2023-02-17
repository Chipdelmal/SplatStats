#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sys import argv
from os import path
import SplatStats as splat

(iPath, oPath) = (
    path.expanduser('~/Documents/Sync/BattlesDocker/battles'),
    path.expanduser('~/Documents/Sync/BattlesDocker/out')
)
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Team Object
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'Oswal　ウナギ', 
    'April ウナギ', 'Rei ウナギ', 'DantoNnoob', 'Murazee'
)
team = splat.Team(NAMES, bPaths, timezone='America/Los_Angeles')
###############################################################################
# Battles Analysis
###############################################################################
plyr = 'čħîþ ウナギ'

btleHist = team.battleHistory
btleDates = btleHist['datetime'].unique()

mType = 'Rainmaker'

ix = 1
btl = team.players[plyr].battleRecords[ix]
btlType = btl.matchType
(btlAllies, btlEnemies) = (
    set(btl.alliedTeam['player name']), 
    set(pd.concat(btl.enemyTeams)['player name'])
)
(btlResult, btlKO) = (
    (True if btl.alliedTeam['win'].iloc[0]!='L' else False),
    btl.ko
)

