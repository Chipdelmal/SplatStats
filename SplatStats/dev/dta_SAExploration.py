#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os    
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import numpy as np
from os import path
from sys import argv
import SplatStats as splat
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt


if splat.isNotebook():
    (plyrName, weapon, mode, overwrite) = ('čħîþ ウナギ', 'All', 'All', 'False')
    (iPath, bPath, oPath) = (
        path.expanduser('/Users/sanchez.hmsc/Documents/BattlesDocker/jsons'),
        path.expanduser('/Users/sanchez.hmsc/Documents/BattlesDocker/battles'),
        path.expanduser('/Users/sanchez.hmsc/Documents/BattlesDocker/out')
    )
    fontPath = '/Users/sanchez.hmsc/Documents/GitHub/SplatStats/other/'
else:
    (plyrName, weapon, mode, overwrite) = argv[1:]
    (iPath, bPath, oPath) = (
        '/data/jsons', 
        '/data/battles', 
        '/data/out'
    )
    fontPath = '/other/'
overwrite = (True if overwrite=="True"  else False)
LEN_LIMIT = 400
###############################################################################
# Auxiliary 
###############################################################################
title = '(Kills+0.5*Assists)/Deaths'
fNameID = f'{plyrName}-{weapon}'
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=overwrite)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Player Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
playerHistory = playerHistory[playerHistory['match mode']!='PRIVATE']
# Weapon filter ---------------------------------------------------------------
if weapon!='All':
    playerHistory = playerHistory[playerHistory['main weapon']==weapon]
else:
    playerHistory = playerHistory
###############################################################################
# Initial Explorations 
###############################################################################
stat='kad'
results = []
(delta, xlim) = (0.1, 20)
for threshold in np.arange(0, xlim+delta, delta):
    (won, lost) = [playerHistory[playerHistory['winBool']==i] for i in (1, 0)]
    (wonCount, lostCount) = (
        won[won[stat]>=threshold].shape[0],
        lost[lost[stat]>=threshold].shape[0]
    )
    ratio = (wonCount+lostCount) and wonCount / (wonCount+lostCount) or 0
    results.append((threshold, ratio))

(fig, ax) = plt.subplots(figsize=(10, 4))
ax.bar(
    [i[0] for i in results], 
    [i[1] for i in results],
    width=delta
)
ax.set_xlim(0, xlim)
ax.set_ylim(0, 1)
ax.set_xlabel(stat)
ax.set_ylabel('win ratio')