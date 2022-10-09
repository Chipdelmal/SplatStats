#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import SplatStats as splat
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from SplatStats.constants import MKR_STATS


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
LEN_LIMIT = 400
###############################################################################
# Create Player Objects
##############################################################################
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'DantoNnoob',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 'Rei ウナギ'
)
name = 'čħîþ ウナギ'
for name in NAMES:
    plyr = splat.Player(name, bPaths, timezone='America/Los_Angeles')
    playerHistory = plyr.battlesHistory
    phLen = playerHistory.shape[0]
    if phLen > LEN_LIMIT:
        ilocRange = (-LEN_LIMIT, phLen)
    else:
        ilocRange = (0, -1)
    ###########################################################################
    # Histogram
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(30, 15))
    (fig, ax) = splat.plotKillsAndDeathsHistogram(
        (fig, ax), playerHistory, (0, 40), yRange=(-.25, .25), edgecolor='k',
        normalized=True
    )
    plt.savefig(
        path.join(oPath, f'Histogram - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    # Battle History
    ###########################################################################
    yRange = ((0, 40), (0, 2000))
    fig = plt.figure(figsize=(30, 5))
    gs = fig.add_gridspec(
        2, 1,  
        width_ratios=(1, ), height_ratios=(.75, .05),
        left=0.1, right=0.9, bottom=0.1, top=0.9,
        wspace=0.05, hspace=0
    )
    ax_top    = fig.add_subplot(gs[0])
    ax_bottom = fig.add_subplot(gs[1], sharex=ax_top)
    (_, ax_top) = splat.plotMatchHistory(
        (fig, ax_top), playerHistory, 
        yRange=yRange, sizeMultiplier=.8, ilocRange=ilocRange
    )
    (_, ax_bottom) = splat.plotMatchTypeHistory(
        (fig, ax_bottom), playerHistory, 
        sizeMultiplier=.7, labelsize=4, ilocRange=ilocRange
    )
    ax_top.tick_params(labelbottom=False)
    ax_bottom.set_yticks([])
    plt.setp(ax_bottom.get_xticklabels(), rotation=90, ha='right')
    plt.savefig(
        path.join(oPath, f'History - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    # Iris
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    (fig, ax) = splat.plotkillDeathIris(
        (fig, ax), playerHistory,
        # colorsTop=('#4F55ED', '#CB0856'),
        # colorBars='#4F55ED',
        innerGuides=(0, 6, 1), outerGuides=(10, 50, 10),
        fontColor='#00000066',
        innerGuidesColor="#00000033",
        outerGuidesColor="#00000011",
        frameColor="#000000AA"
    )
    ax.set_facecolor("w")
    fig.savefig(
        path.join(oPath, f'Iris - {plyr.name}.png'), 
        dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
###############################################################################
# Legend
###############################################################################
(fig, ax) = plt.subplots(figsize=(1, 5))
(fig, ax) = splat.generateMatchHistoryLegend((fig, ax))
plt.savefig(
    path.join(oPath, 'Legend.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()