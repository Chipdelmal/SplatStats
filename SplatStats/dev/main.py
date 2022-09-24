#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import markers
from collections import Counter

if splat.isNotebook():
    (iPath, oPath) = (
        '/home/chipdelmal/Documents/GitHub/s3s/',
        '/home/chipdelmal/Documents/GitHub/SplatStats/BattlesData'
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Create Player Objects
###############################################################################
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 'DantoNnoob'
)
plyr = splat.Player(NAMES[0], bPaths, timezone='America/Los_Angeles')
# (chip, yami, april, richie, memo, tomas) = [
#     splat.Player(nme, bPaths, timezone='America/Los_Angeles')
#     for nme in NAMES
# ]
# team = (chip, yami, april, richie, memo, tomas)
playerHistory = plyr.battlesHistory
plyr.playerStats