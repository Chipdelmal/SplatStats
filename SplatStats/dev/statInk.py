# !/usr/bin/env python3

import numpy as np
from os import path
from sys import argv
from glob import glob
from random import shuffle
import matplotlib.pyplot as plt
import SplatStats as splat


if splat.isNotebook():
    (six, USR) = (2, 'dsk')
    GMODE = 'All'
else:
    (six, GMODE) = argv[1:]
    six = int(six)
SSON = ['Drizzle Season 2022', 'Chill Season 2022', 'Fresh Season 2023']
SEASON = SSON[six]
###############################################################################
# Constants
###############################################################################
GMODES = {'Clam Blitz', 'Splat Zones', 'Tower Control', 'Turf War', 'Rainmaker'}
FNSTR = '{} ({}) - '.format(SEASON, GMODE)
if GMODE in GMODES:
    POLAR = {
        'fontSizes': (12, 10), 'ticksStep': 1,
        'yRange': (0, 75e3), 'rRange': (0, 90)
    }
    PART_SCALER = ['k', 1e3]
    TITLES = True
else:
    POLAR = {
        'fontSizes': (12, 3.75), 'ticksStep': 4,
        'yRange': (0, 300e3), 'rRange': (0, 180),
        'topRank': None
    }
    PART_SCALER = ['M', 1e6]
    TITLES = True
###############################################################################
# Get files and set font
###############################################################################
if splat.isNotebook():
    if USR=='lab':
        DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
    elif USR=='lap':
        DATA_PATH = '/Users/sanchez.hmsc/Documents/SyncMega/BattlesDocker'
    else:
        DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
else:
    DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
COLORS = splat.ALL_COLORS
shuffle(COLORS)
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
###############################################################################
# Filter by Constraints
###############################################################################
if GMODE in GMODES:
    fltrs = (btls['season']==SEASON, btls['mode']==GMODE)
    fltrBool = [all(i) for i in zip(*fltrs)]
    btlsFiltered = btls[fltrBool]
else:
    GMODE = 'All'
    fltrs = (btls['season']==SEASON, )
    fltrBool = [all(i) for i in zip(*fltrs)]
    btlsFiltered = btls[fltrBool] 
###############################################################################
# Get Total Season Frequencies and Dominance Matrix
###############################################################################
(wpnFreq, wpnWLT, lbyFreq, lbyDaily) = (
    splat.getWeaponsFrequencies(btlsFiltered),
    splat.getWeaponsWLT(btlsFiltered),
    splat.getLobbyFrequencies(btlsFiltered),
    splat.countDailyLobbies(btlsFiltered)
)
lbyGaussDaily = splat.smoothCountDailyLobbies(lbyDaily)
(mNames, mMatrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
(sNames, sMatrix, sSort) = splat.normalizeDominanceMatrix(mNames, mMatrix)
# Calculate auxiliary metrics -------------------------------------------------
wpnRank = splat.rankWeaponsFrequency(wpnFreq, wpnWLT)
(mWpnWins, mWpnLoss) = (
    np.sum(mMatrix, axis=1)/4, 
    np.sum(mMatrix, axis=0)/4
)
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
# Plot Total Frequencies
###############################################################################
fName = FNSTR+'Polar.png'
if GMODE in GMODES:
    POLAR['topRank'] = (len(wpnRank)-20, len(wpnRank))
(fig, ax) = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})
(fig, ax) = splat.plotPolarFrequencies(
    wpnFreq, wpnRank, figAx=(fig, ax),
    fontSizes=POLAR['fontSizes'], ticksStep=POLAR['ticksStep'],
    yRange=POLAR['yRange'], rRange=POLAR['rRange'],
    topRank=POLAR['topRank']
)
if TITLES:
    partp = np.sum(list(wpnFreq.values()))
    if GMODE in GMODES:
        fstr = '{} ({:.0f}{})'.format(GMODE, partp/PART_SCALER[1], PART_SCALER[0])
    else:
        fstr = 'Participation: {:.2f}{}'.format(partp/PART_SCALER[1], PART_SCALER[0])
    ax.text(
        0.5, 0.48, fstr,
        fontsize=20,
        horizontalalignment='right',
        verticalalignment='top',
        rotation=0,
        transform=ax.transAxes
    )
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###########################################################################
# Weapon Matrix
###########################################################################
fName = FNSTR+'Matrix.png'
COLS = (
    ('#D01D79', '#1D07AC'), 
    ('#6BFF00', '#1D07AC'),
    ('#DACD12', '#1D07AC'),
)
cPal = splat.colorPaletteFromHexList([COLS[six][0], '#FFFFFF', COLS[six][1]])
(fig, ax) = plt.subplots(figsize=(20, 20))
(fig, ax) = splat.plotDominanceMatrix(
    sNames, sMatrix, sSort, mMatrix,
    figAx=(fig, ax), vRange=(-0.75, 0.75), cmap=cPal
)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Gaussian Lobby
###############################################################################
if GMODE not in GMODES:
    fName = FNSTR+'Mode.png'
    (fig, ax) = (plt.figure(figsize=(20, 3)), plt.axes())
    (fig, ax) = splat.plotGaussianLobby(lbyDaily, lbyGaussDaily)
    plt.savefig(
        path.join(DATA_PATH, 'statInk/'+fName),
        dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
    )
    plt.close('all')
###############################################################################
# Lobby Type
###############################################################################
if GMODE not in GMODES:
    fName = FNSTR+'Lobby.png'
    (fig, ax) = plt.subplots(figsize=(0.4, 20))
    (fig, ax) = splat.barChartLobby(lbyFreq)
    plt.savefig(
        path.join(DATA_PATH, 'statInk/'+fName), dpi=350, 
        transparent=False, facecolor='#ffffff', bbox_inches='tight'
    )
    plt.close('all')