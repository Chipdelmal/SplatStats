#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os    
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import numpy as np
from os import path
from sys import argv
from math import ceil, floor
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
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'Oswal　ウナギ',
    'April ウナギ', 'Rei ウナギ', 'DantoNnoob', 'Murazee', 'HSR'
)
for plyrName in NAMES:
    ###############################################################################
    # Auxiliary 
    ###############################################################################
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

    playerHistory['kad2'] = ((playerHistory['kill']+0.5*playerHistory['assist'])) / [max(i, 1) for i in playerHistory['death']]

    results = []
    (delta, xlim, cumFreq) = (0.5 , 24.5, False)
    totalMatches = playerHistory.shape[0]
    for threshold in np.arange(0, xlim+delta, delta):
        (won, lost) = [playerHistory[playerHistory['winBool']==i] for i in (1, 0)]
        (wonCount, lostCount) = (
            won[won[stat]>=threshold].shape[0],
            lost[lost[stat]>=threshold].shape[0]
        )
        ratio = (wonCount+lostCount) and wonCount / (wonCount+lostCount) or 0
        totRange = sum((playerHistory[stat]>=threshold)&(playerHistory[stat]<threshold+delta))
        if cumFreq:
            matchFreq = (wonCount+lostCount)/totalMatches
        else:
            matchFreq = totRange/totalMatches
        results.append((threshold, ratio, matchFreq))
    top = min([i[0] for i in results if i[1]==0])

    (fig, ax) = plt.subplots(figsize=(10, 3))
    ax.bar(
        [i[0] for i in results], 
        [i[1] for i in results],
        width=delta, color='#502EBAAA'
    )
    for (x, v, f) in results:
        if (v>0) and (f<1):
            ax.hlines([f, ], x-delta/2, x+delta/2, color='#CB0856EE', lw=2)
    ax.bar(
        np.arange(top, xlim+delta, delta), 
        [1]*len(np.arange(top, xlim+delta, delta)),
        width=delta, color='#7F7F9955'
    )
    ax.vlines(
        np.arange(-delta/2, xlim+delta/2, 1), 
        ymin=0, ymax=1, zorder=10, 
        color='#000000CC', lw=1
    )
    ax.set_xticks(np.arange(0-delta/2, xlim+delta, 1))
    ax.set_xticklabels([floor(i)+1 for i in np.arange(0-delta/2, xlim+delta, 1)])
    # ax.set_xticks(np.arange(0+delta/2, xlim+delta/2, 1))
    # ax.set_xticklabels([int(i) for i in np.arange(0, xlim, 1)])
    ax.set_xlim(-delta/2, xlim+delta/2)
    ax.set_ylim(0, 1)
    ax.set_xlabel(stat)
    ax.set_ylabel('win ratio')
    ax.grid(False)
    fig.savefig(
        path.join(oPath, f'{fNameID}_RateKAD.png'), 
        dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor()
    )