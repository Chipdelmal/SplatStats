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
won = playerHistory[playerHistory['winBool']==1]
won[((won['kill']+0.5*won['assist'])/won['death']>=1.5)]


threshold = 0.5

(won, lost) = [playerHistory[playerHistory['winBool']==i] for i in (1, 0)]
(wonCount, lostCount) = (
    won[won['kad']>=threshold].shape[0],
    lost[lost['kad']>=threshold].shape[0]
)
wonCount/lostCount
