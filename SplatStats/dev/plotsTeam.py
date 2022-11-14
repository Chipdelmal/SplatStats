#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import SplatStats as splat
import matplotlib.pyplot as plt


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################a
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
(fig, ax) = splat.plotStreamTeam(
    (fig, ax), team, teamHistBT,
    colors = [
        "#0D40DE", "#EC0B68", "#6ABF0B", "#9090BA",
        "#A577FF", "#941A88", "#CFD1C7", "#E4E567" 
    ]
)
fig.savefig(
    path.join(oPath, f'Wave - Team.png'), 
    dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor()
)
