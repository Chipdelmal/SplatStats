#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sys import argv
from os import path
import SplatStats as splat
import matplotlib.pyplot as plt
from SplatStats.Player import Player
from SplatStats.constants import MKR_STATS


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Create Player Objects
##############################################################################
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'Oswal　ウナギ', 
    'April ウナギ', 'Rei ウナギ', 'DantoNnoob', 'Murazee'
)
tz = 'America/Los_Angeles'
plyrs = {name: splat.Player(name, bPaths, timezone=tz) for name in NAMES}
# Players aggregate -----------------------------------------------------------
df = pd.concat([plyrs[nme].battlesHistory for nme in NAMES], axis=0)
playerHistory = df # plyrs[NAMES[0]].battlesHistory
playerHistory['matches'] = [1]*playerHistory.shape[0]
playerHistory['win bool'] = np.asarray([i=='W' for i in playerHistory['win']])
dailyHistory = playerHistory.groupby(
    playerHistory['datetime'].dt.floor('h')
).sum()
dailyHistory.sum()
# Date-sorted -----------------------------------------------------------------
datesSet = [set(plyrs[nme].battlesHistory['datetime']) for nme in NAMES]
dates = sorted(list(set.union(*datesSet)))