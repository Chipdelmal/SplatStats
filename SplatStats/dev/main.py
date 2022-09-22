#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import markers

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
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
chip    = splat.Player('čħîþ ウナギ', bPaths, id=7293)
yami    = splat.Player('Yami ウナギ', bPaths, id=None)
# april   = splat.Player('April ウナギ', bPaths, id=None)
# richie  = splat.Player('Riché ウナギ', bPaths, id=None)
# memo    = splat.Player('Oswal　ウナギ', bPaths, id=None)
# tomas   = splat.Player('Murazee', bPaths, id=None)
# Group players for iterations ------------------------------------------------
# team = (chip, yami, april, richie, memo, tomas)
###############################################################################
# Process Player
###############################################################################
plyr = chip
playerHistory = plyr.battlesHistory
plyr.calcPlayerStats()
###############################################################################
# Plot K/D ratio
###############################################################################
timeScale = False
cats = (
    'kill', 'death', 'match type', 'main weapon', 
    'win', 'special', 'paint', 'assist'
)
(kill, death, matchType, weapon, win, special, paint, assist) = [
    list(playerHistory[cat]) for cat in cats
]
dates = list(playerHistory['datetime'])
hoursDiff = [(d-min(dates)).seconds/3600  for d in dates]
ymax = max(max(kill), max(death))
# Use match type for point shape ----------------------------------------------
mNum = len(matchType)
(fig, ax) = plt.subplots(figsize=(30, 15))
for i in range(mNum):
    # Get shape and color for markers and lines -------------------------------
    shape = 'o' if matchType[i] != 'Turf War' else 'o'
    color = 'blue' if kill[i] >= death[i] else 'red'
    colorMT = 'white' if matchType[i] == 'Turf War' else 'purple'
    colorWL = 'green' if win[i] == 'W' else 'red'
    shapeWL = r'$\uparrow$' if win[i] == 'W' else r'$\downarrow$'
    shapeMT = "1" if matchType[i] != 'Turf War' else '-'
    xPos = hoursDiff[i] if timeScale else i
    # Plot kill to death range ------------------------------------------------
    ax.plot(xPos, kill[i], 'o', color=color, alpha=0.35, zorder=1)
    ax.plot(xPos, death[i], 'X', color=color, alpha=0.35, zorder=1)
    ax.vlines(xPos, kill[i], death[i], color=color, alpha=0.2, zorder=2)
    # Specials and W/L --------------------------------------------------------
    ax.plot(xPos, special[i], "_", color='k', alpha=0.1, zorder=0)
    ax.plot(xPos, assist[i], ".", color='k', alpha=0.1, zorder=0)
    ax.plot(xPos, -1, marker=shapeWL, color=colorWL, alpha=0.3, zorder=0, markersize=10)
    pnt = np.interp(paint[i], [0, max(paint)], [0, ymax])
    ax.add_patch(Rectangle((xPos-.5, 0), 1, pnt, facecolor='magenta', alpha=.05, zorder=-5))
    # Plot vspan for match type -----------------------------------------------
    ax.plot(xPos, ymax+1, shapeMT, color='k', alpha=0.2, zorder=0)
    # ax.axvspan(xPos-.5, xPos+.5, color=colorMT, alpha=.05, lw=0, zorder=-10)
    # ax.vlines(
    #     [xPos], 0, 1, color=colorWL, alpha=.1,
    #     transform=ax.get_xaxis_transform(), zorder=-15
    # )
# ax.hlines([0], 0, 1, color='k', transform=ax.get_yaxis_transform())
xLim = max(hoursDiff) if timeScale else mNum
ax.set_xlim(-.5, xLim-.5)
# ax.set_ylim(-2, max(max(kill), max(death))+2)
ax.set_ylim(-2, ymax+2)
ax.set_aspect(.25/ax.get_data_ratio())
ax.set_xticks(list(range(mNum)))
plt.xticks(rotation=90)
ax.set_xticklabels(weapon)
kLv = range(0, ymax+5, 5)
pLv = [np.interp(i, [0, ymax], [0, max(paint)]) for i in kLv]
ax.set_yticks(kLv)
ax.set_yticklabels([f'{i}/{round(p)}' for (i, p) in zip(kLv, pLv)])
plt.savefig(
    path.join(oPath, (chip.name)+'-BHistory.png'), 
    dpi=300, bbox_inches='tight'
)

