#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib import font_manager

if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s_source/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Setup Splats Font
###############################################################################
try:
    bPaths = splat.getBattleFilepaths(oPath)
    font_dirs = [oPath]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    plt.rcParams["font.family"]="Splatfont 2"
except:
    pass
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
teamHistBT = team.reshapeTeamHistoryByPeriod(
    period='24H'
)
###############################################################################
# Plotting Stream
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 2))
(fig, ax) = splat.plotStreamTeam((fig, ax), team, teamHistBT, colors=COLORS)
fig.savefig(
    path.join(oPath, f'Wave - Team.png'), 
    dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()