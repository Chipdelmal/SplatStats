# !/usr/bin/env python3

# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

from os import path, system
from glob import glob
import numpy as np
import pandas as pd
from random import shuffle
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
import SplatStats as splat


(six, USR) = (1, 'dsk')
SSON = ['Drizzle Season 2022', 'Chill Season 2022', 'Fresh Season 2023']
SEASON = SSON[six]
TOP = 20
###############################################################################
# Get files and set font
###############################################################################
if USR=='lab':
    DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
elif USR=='lap':
    DATA_PATH = '/Users/sanchez.hmsc/Documents/SyncMega/BattlesDocker'
else:
    DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
###############################################################################
# Filter by Constraints
###############################################################################
fltrs = (btls['season']==SEASON, )
fltrBool = [all(i) for i in zip(*fltrs)]
btlsFiltered = btls[fltrBool]
###############################################################################
# Get Total Season Frequencies and Dominance Matrix
###############################################################################
(wpnFreq, wpnWLT, lbyFreq) = (
    splat.getWeaponsFrequencies(btlsFiltered),
    splat.getWeaponsWLT(btlsFiltered),
    splat.getLobbyFrequencies(btlsFiltered)
)
(mNames, mMatrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
(mWpnWins, mWpnLoss) = (np.sum(mMatrix, axis=1)/4, np.sum(mMatrix, axis=0)/4)
# Checks for consistency ------------------------------------------------------
tests = [
    np.sum(list(wpnFreq.values()))/8 == btlsFiltered.shape[0],
    np.sum(list(lbyFreq.values()))   == btlsFiltered.shape[0],
    np.sum(np.sum(wpnWLT[1][:,2]))   == np.sum(list(wpnFreq.values())),
    all(mWpnWins == wpnWLT[1][:,0]),
    all(mWpnLoss == wpnWLT[1][:,1]),
    all(wpnWLT[1][:,2] == mWpnWins+mWpnLoss)
]
assert(all(tests))
###############################################################################
# Calculate Auxiliary Metrics
###############################################################################
wpnsNum = len(mNames)
freqSorting = [mNames.index(w) for w in wpnFreq.keys()]
wpnWinRatio = wpnWLT[1][:,0]/wpnWLT[1][:,2]
###############################################################################
# Plot Total Frequencies
###############################################################################
itr = zip(
    [wpnsNum-i for i in range(wpnsNum)], 
    wpnFreq.keys(),
    [wpnWinRatio[ix] for ix in freqSorting]
)
labels = ['{:02d}. {} ({}%)'.format(ix, n, int(f*100)) for (ix, n, f) in itr]
COLORS = splat.ALL_COLORS
shuffle(COLORS)
(fig, ax) = plt.subplots(
    figsize=(12, 12), subplot_kw={"projection": "polar"}
)
(fig, ax) = splat.polarBarChart(
    labels[::-1], list(wpnFreq.values())[::-1],
    yRange=(0, 3.0e5), rRange=(0, 180), ticksStep=4,
    colors=[c+'DD' for c in COLORS],
    edgecolor='#00000088', linewidth=0,
    figAx=(fig, ax),
    ticksFmt={
        'lw': 1, 'range': (-.2, 1), 
        'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.1e}'
    },
    labelFmt={
        'color': '#000000EE', 'fontsize': 3.75, 
        'ha': 'left', 'fmt': '{:.1f}'
    }
)
xlabels = ax.get_xticklabels()
for txt in xlabels:
    lab = txt.get_text()
    txt.set_text('{:.0f}k'.format(float(lab)/1e3))
ax.set_xticklabels(xlabels, rotation=0, fontsize=8)
fName = 'Polar - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')