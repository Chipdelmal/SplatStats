#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sys import argv
from os import path
import SplatStats as splat

plyrName = 'čħîþ ウナギ'
(iPath, bPath, oPath) = (
    path.expanduser('~/Documents/Sync/BattlesDocker/jsons'),
    path.expanduser('~/Documents/Sync/BattlesDocker/battles'),
    path.expanduser('~/Documents/Sync/BattlesDocker/out')
)
fontPath = '/home/chipdelmal/Documents/GitHub/SplatStats/other/'
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=True)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Team Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
###############################################################################
# Battles Analysis
###############################################################################
btleHist = plyr.battleRecords

matchType = 'Rainmaker'

ix = 0
# Get battle entry ------------------------------------------------------------
btl = btleHist[ix]
# Get teams dataframes and result ---------------------------------------------
(dfAlly, dfEnmy) = (btl.alliedTeam, pd.concat(btl.enemyTeams))
(btlResult, btlKO) = (
    (True if btl.alliedTeam['win'].iloc[0]!='L' else False),
    btl.ko
)
# Team weapons ----------------------------------------------------------------
(wpAlly, wpEnmy) = [list(i['main weapon']) for i in (dfAlly, dfEnmy)]