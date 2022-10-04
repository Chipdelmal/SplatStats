#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
import SplatStats as splat
from pywaffle import Waffle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
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
    'Oswal　ウナギ', 'April ウナギ', 'Murazee'
)
plyr = splat.Player(NAMES[0], bPaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
playerHistory.shape
###############################################################################
# Dev
###############################################################################
stagesStatsMatch = splat.calcStagesStatsByType(playerHistory)
# stagesDF = splat.calcStagesStats(playerHistory)
stagesDF = stagesStatsMatch['Rainmaker']

(fig, ax) = plt.subplots(figsize=(5, 5))
(fig, ax) = splat.plotTreemapByStages(
    (fig, ax), stagesDF, metric='kassists ratio', 
    fmt='{:.2f}', pad=0.1
)


fig = plt.figure(
    FigureClass=Waffle,
    rows=20, 
    columns=20,
    values=stagesDF['win ratio']*100,
    labels=list(stagesDF['stage']),
    starting_location='NW',
    vertical=True,
    block_arranging_style='snake',
    colors=[splat.CLR_STAGE[s] for s in list(stagesDF['stage'])],
    # labels=[f"{k} ({int(v / sum(data.values()) * 100)}%)" for k, v in data.items()],
    legend={
        'loc': 'upper left',
        'bbox_to_anchor': (1, 1),
        'ncol': 1,
        'framealpha': 0,
        'fontsize': 12
    }
)
