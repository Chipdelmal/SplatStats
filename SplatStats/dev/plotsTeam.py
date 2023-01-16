#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# Setup Splats Font
###############################################################################
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=True)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Team Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'Oswal　ウナギ',
    'April ウナギ', 'Rei ウナギ', 'DantoNnoob', 'Murazee', 'HSR'
)
COLORS = (
    "#0D40DE", "#EC0B68", "#6ABF0B", "#A577FF",
    "#D645C8", "#941A88", "#CFD1C7", "#E4E567", 
    '#8CE47F'
)
TZ = 'America/Los_Angeles'
team = splat.Team(NAMES, bPaths, TZ)
teamHist = team.battleHistory
teamHistBT = team.reshapeTeamHistoryByPeriod(period='24H')
###############################################################################
# Plotting Stream
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 2))
(fig, ax) = splat.plotStreamTeam((fig, ax), team, teamHistBT, colors=COLORS)
fig.savefig(
    path.join(oPath, f'Team-Wave.png'), 
    dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()