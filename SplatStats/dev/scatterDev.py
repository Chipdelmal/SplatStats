#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyBboxPatch
from colorutils import Color

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
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 
    'DantoNnoob'
)
plyr = splat.Player(NAMES[6], bPaths, timezone='America/Los_Angeles')
# (chip, yami, april, richie, memo, tomas) = [
#     splat.Player(nme, bPaths, timezone='America/Los_Angeles')
#     for nme in NAMES
# ]
# team = (chip, yami, april, richie, memo, tomas)
playerHistory = plyr.battlesHistory
###############################################################################
# Plot K/D ratio
###############################################################################
timeScale = False
cats = (
    'kill', 'death', 'match type', 'main weapon', 
    'win', 'special', 'paint', 'assist', 'splatfest', 'ko'
)
(kill, death, matchType, weapon, win, special, paint, assist, splatfest, ko) = [
    list(playerHistory[cat]) for cat in cats
]
dates = list(playerHistory['datetime'])
hoursDiff = [(d-min(dates)).seconds/3600  for d in dates]
ymax = max(max(kill), max(death))
kLv = range(0, ymax+5, 5)
# Use match type for point shape ----------------------------------------------
mNum = len(matchType)
(fig, ax) = plt.subplots(figsize=(30, 15))
for i in range(mNum):
    # Get shape and color for markers and lines -------------------------------
    shape = 'o' if matchType[i] != 'Turf War' else 'o'
    color = splat.CLR_KILL_DEATH['kill'] if kill[i] >= death[i] else splat.CLR_KILL_DEATH['death']
    # colVal = splat.mapNumberToSaturation(abs(kill[i]-death[i]), color, satLims=(.5, 1, 1)) 
    colorMT = splat.CLR_MT[matchType[i]]
    colorWL = splat.CLR_WL[win[i]]
    shapeWL = "^" if win[i] == 'W' else "v"
    shapeMT = splat.MKR_MT[matchType[i]]
    xPos = hoursDiff[i] if timeScale else i
    # Plot kill to death range ------------------------------------------------
    ax.plot(xPos, kill[i], 'o', color=color, alpha=0.35, ms=4, zorder=1)
    ax.plot(xPos, death[i], 'X', color=color, alpha=0.35, ms=4, zorder=1)
    ax.vlines(xPos, kill[i], death[i], color=color, alpha=0.2, zorder=2)
    # Specials and W/L --------------------------------------------------------
    ax.plot(xPos, special[i], "_", color='k', alpha=0.1, zorder=0)
    ax.plot(xPos, assist[i], ".", color='k', alpha=0.1, zorder=0)
    if ko[i]:
        ax.plot(xPos, -1.25, marker=".", color=colorWL, alpha=0.25, zorder=0, markersize=2.5)
    ax.plot(xPos, -.75, marker=shapeWL, color=colorWL, alpha=0.3, zorder=0, markersize=5)
    pnt = np.interp(paint[i], [0, max(paint)], [0, ymax])
    # Paint -------------------------------------------------------------------
    ax.add_patch(Rectangle((xPos-.5, 0), 1, pnt, facecolor=splat.CLR_PAINT, alpha=.075, zorder=-5))
    # Plot vspan for match type -----------------------------------------------
    # ax.plot(xPos, max(kLv)-1, shapeMT, color=colorMT, alpha=0.3, zorder=0)
    ax.plot(xPos, -1.75, shapeMT, color=colorMT, alpha=0.3, zorder=0)
    if splatfest[i]:
        # ax.plot(xPos, max(kLv)-1, '.', color='r', alpha=0.2, zorder=0, ms=1.25)
        ax.plot(xPos, -1.75, '.', color='r', alpha=0.2, zorder=0, ms=1.25)
xLim = max(hoursDiff) if timeScale else mNum
for i in range(0, ymax-1, 5):
    ax.hlines(
        i, 0, 1, 
        color='k', ls='--', alpha=.125, lw=.75,
        transform=ax.get_yaxis_transform(), zorder=-50
    )
# Stats -----------------------------------------------------------------------
stats = plyr.playerStats
avg = stats['kpads avg']
(kill, death, assist) = (avg['kills'], avg['deaths'], avg['assist'])
(win, loss) = (stats['general']['win'], stats['general']['loss'])
adjRatio = (kill+0.5*assist)/(death)
pA = f"(kills [{kill:.2f}] + 0.5*assists [{assist:.2f}])/(deaths [{death:.2f}]) = {adjRatio:.2f}"
pB = f"paint [{avg['paint']:.2f}] & special [{avg['special']:.2f}]"
pC = f"wins [{win}]/losses [{loss}] = {win/loss:.2f} in {win+loss} matches"
# ax.hlines([0], 0, 1, color='k', transform=ax.get_yaxis_transform())
# ax.set_facecolor('#EFF2EB')
ax.set_xlim(-.5, xLim-.5)
# ax.set_ylim(-2, max(max(kill), max(death))+2)
ax.set_ylim(-2.5, ymax+2)
ax.set_aspect(.25/ax.get_data_ratio())
ax.set_xticks(list(range(mNum)))
plt.xticks(rotation=90)
ax.tick_params(axis='x', which='major', labelsize=5)
ax.set_xticklabels(weapon)
for i in range(0, xLim, 10):
    ax.vlines(
        i, 0, max(kLv)+2, 
        color='k', ls='--', alpha=.125, lw=.75,
        # transform=ax.get_xaxis_transform(), 
        zorder=-50
    )
pLv = [np.interp(i, [0, ymax], [0, max(paint)]) for i in kLv]
ax.set_yticks(kLv)
ax.set_yticklabels([f'{i:02d} ({round(p):04d})' for (i, p) in zip(kLv, pLv)])
pName = plyr.name.split(' ')[0]
plt.title(pName+'\n'+pA+'         '+pC+'        '+pB)
plt.savefig(
    path.join(oPath, (plyr.name)+' BHistory.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)

