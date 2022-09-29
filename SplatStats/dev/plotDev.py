#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import SplatStats as splat
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


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
# Plot Dev
###############################################################################
yRange = (0, 40)
fig = plt.figure(figsize=(30, 5))
gs = fig.add_gridspec(
    2, 1,  
    width_ratios=(1, ), height_ratios=(.75, .04),
    left=0.1, right=0.9, bottom=0.1, top=0.9,
    wspace=0.05, hspace=0
)
ax_top    = fig.add_subplot(gs[0])
ax_bottom = fig.add_subplot(gs[1], sharex=ax_top)
(_, ax_top) = splat.plotMatchHistory((fig, ax_top), playerHistory)
(_, ax_bottom) = splat.plotMatchTypeHistory((fig, ax_bottom), playerHistory)
ax_top.tick_params(labelbottom=False) 
plt.setp(ax_bottom.get_xticklabels(), rotation=90, ha='right')
plt.savefig(
    path.join(oPath, (plyr.name)+' BHistoryNew.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)



figAx = plt.subplots(figsize=(30, 15))
labelsize=5 
alphaMultiplier=1 
sizeMultiplier=1
yRange = (0, 50)

(fig, ax) = figAx
axR = ax.twinx()
# Retreiving data ---------------------------------------------------------
(AM, SM) = (alphaMultiplier, sizeMultiplier)
(PHIST, MNUM) = (playerHistory, playerHistory.shape[0])
CATS = ('kill', 'death', 'assist', 'special', 'paint')
(kill, death, assist, special, paint) = [np.array(PHIST[cat]) for cat in CATS]
CLR_KD = splat.CLR_STATS
# Main panel ------------------------------------------------------------------
autoRange = (0, max(max(kill), max(death)))
(ymin, ymax) = (yRange if yRange else autoRange)


m = 0
for m in range(MNUM):
    xPos = m
    # Kill/Death
    kd = (kill[m]-death[m])
    clr_kd = (CLR_KD['kill'] if kd >= 0 else CLR_KD['death'])
    ax.plot(xPos, kill[m],  splat.MKR_STATS['kill'], color=clr_kd, alpha=0.35, ms=4, zorder=1)
    ax.plot(xPos, death[m], splat.MKR_STATS['kill'], color=clr_kd, alpha=0.35, ms=4, zorder=1)
    ax.vlines(xPos, kill[m], death[m], color=clr_kd, alpha=0.20, zorder=2)
    # Special/Assist
    ax.plot(xPos, special[m], splat.MKR_STATS['special'], color=CLR_KD['special'], alpha=0.1, zorder=0)
    ax.plot(xPos, assist[m], splat.MKR_STATS['assist'], color=CLR_KD['assist'], alpha=0.1, zorder=0)
    # Paint
    axR.plot(xPos, paint[m], '-', color='#ffffff', alpha=0, zorder=0)
    axR.add_patch(Rectangle(
        (xPos-.5, 0), 1, paint[m], 
        facecolor=splat.CLR_PAINT, alpha=.075, zorder=-5
    ))
ax.set_ylim(0, ymax)
ax.set_xlim(-0.5, MNUM)
splat.align_yaxis(ax, 0, axR, 0)


