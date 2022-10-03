#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
import SplatStats as splat
from pywaffle import Waffle
import squarify
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
# historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
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
###############################################################################
# Dev
###############################################################################
stagesStats = splat.calcStagesStatsByType(playerHistory)
stagesStats['Rainmaker']
stats = splat.calcStagesStats(playerHistory)

list(stats['stage'])

fig = plt.figure(
    FigureClass=Waffle,
    rows=20, 
    columns=20,
    values=stats['win ratio']*100,
    labels=list(stats['stage']),
    starting_location='NW',
    vertical=True,
    block_arranging_style='snake',
    colors=[splat.CLR_STAGE[s] for s in list(stats['stage'])],
    # labels=[f"{k} ({int(v / sum(data.values()) * 100)}%)" for k, v in data.items()],
    legend={
        'loc': 'upper left',
        'bbox_to_anchor': (1, 1),
        'ncol': 1,
        'framealpha': 0,
        'fontsize': 12
    }
)

squarify.plot(
    sizes=stats['win'], 
    label=stats['stage'], 
    alpha=.8 
)
plt.axis('off')
plt.show()