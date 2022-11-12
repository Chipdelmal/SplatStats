#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sys import argv
from os import path
import SplatStats as splat
from scipy import stats
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
from SplatStats.Player import Player
from SplatStats.constants import MKR_STATS


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s/'),
        path.expanduser('~/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Load battle paths
###############################################################################
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Team Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'Oswal　ウナギ',
    'April ウナギ', 'Rei ウナギ', 'DantoNnoob', 'Murazee'
)
COLORS = (
    
)
TZ = 'America/Los_Angeles'
team = splat.Team(NAMES, bPaths, TZ)
teamHist = team.battleHistory
teamHistBT = team.reshapeTeamHistoryByPeriod(
    period='24H'
)
###############################################################################
# Plotting Stream
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 2))
metric = 'kill'
normalized = False
smooth = True
smoothness = 0.75
gridRes = 500
baseline = 'sym'
colors = [
    "#0D40DE", "#EC0B68", "#6ABF0B", "#9090BA",
    "#A577FF", "#941A88", "#CFD1C7", "#E4E567" 
]
# Reshape dataframe and get vars ----------------------------------------------
dfByPlayer = teamHistBT.reorder_levels(["player", "datetime"])
names = team.names
entriesNum = dfByPlayer.loc[names[0]].shape[0]
# Populate stream -------------------------------------------------------------
stream = np.zeros((len(names), entriesNum))
for (ix, name) in enumerate(names):
    stream[ix]  = np.array(dfByPlayer.loc[name][metric])
streamFiltered = stream[:,np.any(stream>0, axis=0)]
# Normalize if needed ---------------------------------------------------------
if normalized:
    cSum = np.sum(streamFiltered, axis=0)
    streamFiltered = np.array([r/cSum for r in streamFiltered])
# Plot variables --------------------------------------------------------------
x = range(streamFiltered.shape[1])
if smooth:
    grid = np.linspace(0, streamFiltered.shape[1], num=gridRes)
    y = [splat.gaussian_smooth(x, i, grid, smoothness) for i in streamFiltered]
else:
    y = streamFiltered
# Generate figure -------------------------------------------------------------
ax.stackplot(grid, y, baseline="sym", colors=COLORS, alpha=.9)
ax.set_xlim(0, max(x))
ax.set_xticks([])
ax.set_yticks([])
# ax.axis('off')
ax.legend(
    names, loc='upper left', frameon=False,
    bbox_to_anchor=(1, 1), ncol=2
)



fig.savefig(
    path.join(oPath, f'Wave.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)