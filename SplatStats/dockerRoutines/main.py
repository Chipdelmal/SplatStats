#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from os import path
from sys import argv
import SplatStats as splat
import matplotlib.pyplot as plt

if splat.isNotebook():
    (plyrName, weapon) = ('čħîþ ウナギ', 'Splattershot')
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s_source/'),
        path.expanduser('~/Desktop/SplatsDocker/')
    )
    fontPath = './SplatStats/'
else:
    (plyrName, weapon) = argv[1:]
    (iPath, oPath) = ('/data/', '/data/')
    fontPath = '/SplatStats/'
fNameID = f'{plyrName}-{weapon}'
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, oPath, overwrite=True)
bFilepaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
if weapon != 'All':
    pHist = playerHistory[playerHistory['main weapon']==weapon]
else:
    pHist = playerHistory
###############################################################################
# Iris
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
(fig, ax) = splat.plotkillDeathIris(
    (fig, ax), pHist,
    alpha=.9,
    innerGuides=(0, 10, 1), outerGuides=(10, 50, 10),
    fontColor='#000000CC', frameColor="#000000AA",
    innerGuidesColor="#000000BB", outerGuidesColor="#000000BB",
    innerTextFmt='{:.2f}'
)
ax.set_facecolor("w")
ax.set_yticklabels(
    ["", 10, 20, 30, 40], 
    fontdict={'fontsize': 8.5, 'color': '#000000BB', 'ha': 'center'}
)
ax.set_rlabel_position(0)
fig.savefig(
    path.join(oPath, f'{fNameID}_Iris.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)