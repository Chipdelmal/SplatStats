#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib import font_manager

if splat.isNotebook():
    (iPath, bPath, oPath) = (
        path.expanduser('~/Documents/BattlesDocker/jsons'),
        path.expanduser('~/Documents/BattlesDocker/battles'),
        path.expanduser('~/Documents/BattlesDocker/out')
    )
    fontPath = path.expanduser('~/Documents/BattlesDocker/')
else:
    (iPath, oPath) = argv[1:]
    fontPath = '~/Documents/BattlesDocker'
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
    "#0D40DEEE", "#EC0B68EE", "#6ABF0BEE", "#A5EEFFEE",
    "#D645C8EE", "#941A88EE", "#CFD1EEC7", "#E4E56EE7", 
    '#8CE47FEE'
)
TZ = 'America/Los_Angeles'
team = splat.Team(NAMES, bPaths, TZ)
teamHist = team.battleHistory
teamHistBT = team.reshapeTeamHistoryByPeriod(period='24H')
###############################################################################
# Plotting Stream
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 2))
(fig, ax) = splat.plotStreamTeam(
    (fig, ax), team, teamHistBT, 
    baseline='sym', colors=COLORS
)
fig.savefig(
    path.join(oPath, f'Team-Wave.png'), 
    dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()