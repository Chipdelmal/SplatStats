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
name = NAMES[0]
for name in NAMES:
    plyr = splat.Player(name, bPaths, timezone='America/Los_Angeles')
    playerHistory = plyr.battlesHistory
    # playerHistory = playerHistory[playerHistory['match type']=='Turf War']
    # Generate Plot
    yRange = ((0, 40), (0, 1600))
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
        (fig, ax_top), playerHistory, yRange=yRange
    )
    (_, ax_bottom) = splat.plotMatchTypeHistory((fig, ax_bottom), playerHistory)
    ax_top.tick_params(labelbottom=False)
    ax_bottom.set_yticks([])
    plt.setp(ax_bottom.get_xticklabels(), rotation=90, ha='right')
    plt.savefig(
        path.join(oPath, (plyr.name)+' BHistoryNew.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
