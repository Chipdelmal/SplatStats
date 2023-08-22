#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from glob import glob
from sys import argv
from os import path
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib import font_manager

if splat.isNotebook():
    (iPath, bPath, oPath) = (
        path.expanduser('~/Documents/Sync/BattlesDocker/jsons'),
        path.expanduser('~/Documents/Sync/BattlesDocker/battles'),
        path.expanduser('~/Documents/Sync/BattlesDocker/out')
    )
    fontPath = '/home/chipdelmal/Documents/GitHub/SplatStats/other/'
else:
    (iPath, oPath) = argv[1:]
    fontPath = '/home/chipdelmal/Documents/GitHub/SplatStats/other/'
    
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=True)
bPaths = splat.getBattleFilepaths(bPath)

NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'DantoNnoob',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 'Rei ウナギ'
)
plyr = splat.Player(NAMES[0], bPaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory