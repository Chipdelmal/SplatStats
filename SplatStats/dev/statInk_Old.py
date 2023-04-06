# !/usr/bin/env python3

# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

from os import path, system
from glob import glob
import pandas as pd
import seaborn as sns
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
import SplatStats as splat
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from collections import Counter


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
btlsFiltered = btls # btls[fltrBool]
###############################################################################
# Get Frequencies
###############################################################################
dfStats = splat.getWeaponsDataframe(btlsFiltered)
weapons = sorted(list(dfStats['weapon'].unique()))
# dfStats['kassist'] = dfStats['kill']+dfStats['assist']/2
dfStats['paint'] = dfStats['inked']/100

(xRan, binSize) = ((0, 25), 1)
stats = ['kill', 'death', 'assist', 'special', 'paint']
(kFreqs, kMeans) = ({}, {})
for wpn in weapons:
    wpnDF = dfStats[dfStats['weapon']==wpn]
    kFreqs[wpn] = splat.getWeaponStatsHistograms(
        wpnDF, xRan, stats=stats, binSize=binSize
    )
    kMeans[wpn] = splat.getWeaponStatsMean(wpnDF, stats=stats, mFun=np.mean)

STATS = {
    'kill': {
        'color': '#1A1AAEDD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        'range': (0, 15)
    },
    'kill': {
        'color': '#1A1AAEDD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        'range': (0, 15)
    },
    'kill': {
        'color': '#1A1AAEDD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        
    },
    'kill': {
        'color': '#1A1AAEDD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
    }
}

STATS = {
    'stat': stats,
    'colors': [
        '#1A1AAEDD', '#801AB3DD', '#C12D74DD', '#1FAFE8DD', '#35BA49DD', 
        '#EE8711DD', '#C12D74DD', '#D645C8DD', 
    ],
    'scalers': [
        lambda x: np.interp(x, [0, k/2, k], [0, .70, 0.95])
        for k in [0.25, 0.25, 1.25, 2, 0.2]
    ],
    'range': [15, 15, 10, 10, 20]
}
STATS['cmaps'] = [
    splat.colorPaletteFromHexList(['#ffffff00', c]) for c in STATS['colors']
]
cconv = mcolors.ColorConverter().to_rgba
bCol = cconv(STATS['colors'][six])
(fig, ax) = plt.subplots(figsize=(5, 20))
for (ix, wFreq) in enumerate(kFreqs):
    for (x, k) in enumerate(wFreq):
        scaled = STATS['scalers'][six](k)
        ax.add_patch(
            Rectangle(
                (x, ix), binSize, 1,
                facecolor=(bCol[0], bCol[1], bCol[2], STATS['scalers'][six](k)),
                edgecolor='#000000AA',
            )
        )
for (ix, wMean) in enumerate(kMeans):
    ax.vlines(
        wMean, ix+0.25, ix+0.75,
        colors='#000000AA',
        lw=2.5, ls='-'
    )
# for (ix, wMedian) in enumerate(kMedians):
#     ax.vlines(
#         wMedian, ix+0.5, ix+1,
#         colors='#00000088',
#         lw=2.5, ls='-'
#     )
ax.set_ylim(0, len(weaponsList))
ax.set_yticks(np.arange(0.5, len(weaponsList), 1))
ax.set_yticklabels(weaponsList)
ax.set_xlim(*xRan)
# ax.xaxis.tick_top()
ax.set_xticks(np.arange(0, STATS['range'][six]+1, 5))
ax.set_title('{}'.format(stat), fontdict={'fontsize': 20})
plt.savefig(
    path.join(DATA_PATH, 'statInk/Weapons-'+stat),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)




six = 0
stat = stats[six]

wk = wpnDF['kill']
splat.calcBinnedFrequencies(wk, 0, 10, 1)

(xMin, xMax, binSize) = (0, 30, 1)
rans = np.arange(xMin, xMax+binSize, binSize)
dSort = sorted(wpnDF['kill'])
ss = np.searchsorted(dSort, rans, side='left')

Counter(dSort)

###############################################################################
# Generate Plot
###############################################################################
STATS = {
    'stat': ['kill', 'death', 'assist', 'special', 'paint'],
    'colors': [
        '#1A1AAEDD', '#801AB3DD', '#C12D74DD', '#1FAFE8DD', '#35BA49DD', 
        '#EE8711DD', '#C12D74DD', '#D645C8DD', 
    ],
    'scalers': [
        lambda x: np.interp(x, [0, k/2, k], [0, .70, 0.95])
        for k in [0.25, 0.25, 1.25, 2, 0.2]
    ],
    'range': [15, 15, 10, 10, 20]
}
STATS['cmaps'] = [
    splat.colorPaletteFromHexList(['#ffffff00', c]) for c in STATS['colors']
]

six = 0
stat = STATS['stat'][six]
weaponsList = weapons[::-1] # ['Splattershot', 'Tentatek Splattershot', 'Hero Shot Replica'] #  # 
(xRan, binSize) = ((0, STATS['range'][six]), 1)
kFreqs = [
    splat.calcBinnedFrequencies(
        dfStats[dfStats['weapon']==wpn][stat], 
        xRan[0], xRan[1], normalized=True
    )
    for wpn in weaponsList
]
kMeans = [
    np.mean(dfStats[dfStats['weapon']==wpn][stat])
    for wpn in weaponsList
]
# kMedians = [
#     np.median(dfStats[dfStats['weapon']==wpn][stat])
#     for wpn in weaponsList
# ]
cconv = mcolors.ColorConverter().to_rgba
bCol = cconv(STATS['colors'][six])
(fig, ax) = plt.subplots(figsize=(5, 20))
for (ix, wFreq) in enumerate(kFreqs):
    for (x, k) in enumerate(wFreq):
        scaled = STATS['scalers'][six](k)
        ax.add_patch(
            Rectangle(
                (x, ix), binSize, 1, 
                # facecolor=STATS['cmaps'][ix%len(STATS['colors'])](scaled),
                facecolor=(bCol[0], bCol[1], bCol[2], STATS['scalers'][six](k)),
                edgecolor='#000000AA',
                # alpha=STATS['scalers'][six](k)
            )
        )
for (ix, wMean) in enumerate(kMeans):
    ax.vlines(
        wMean, ix+0.25, ix+0.75,
        colors='#000000AA',
        lw=2.5, ls='-'
    )
# for (ix, wMedian) in enumerate(kMedians):
#     ax.vlines(
#         wMedian, ix+0.5, ix+1,
#         colors='#00000088',
#         lw=2.5, ls='-'
#     )
ax.set_ylim(0, len(weaponsList))
ax.set_yticks(np.arange(0.5, len(weaponsList), 1))
ax.set_yticklabels(weaponsList)
ax.set_xlim(*xRan)
# ax.xaxis.tick_top()
ax.set_xticks(np.arange(0, STATS['range'][six]+1, 5))
ax.set_title('{}'.format(stat), fontdict={'fontsize': 20})
plt.savefig(
    path.join(DATA_PATH, 'statInk/Weapons-'+stat),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)




(xRan, binSize) = ((0, 20), 1)
wix = weapons.index('Splattershot')
wpn = weapons[wix]
fltrd = dfStats[dfStats['weapon']==wpn]
fltrdStat = [fltrd[i] for i in STATS['stat']]
(fig, ax) = plt.subplots(figsize=(20, 2))
for (ix, st) in enumerate(fltrdStat):
    kFreqs = splat.calcBinnedFrequencies(st, xRan[0], xRan[1], normalized=True)
    for (x, k) in enumerate(kFreqs):
        ax.add_patch(
            Rectangle(
                (x, ix), binSize, 1, 
                facecolor=STATS['cmaps'][ix](k), edgecolor='#000000',
            )
        )
ax.set_title(wpn)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xlim(*xRan)
ax.set_ylim(0, len(STATS['stat']))




kFreqs = splat.calcBinnedFrequencies(fltrd['paint'], 0, 20, normalized=True)




fltrd = dfStats[dfStats['weapon']==wpn]
fltrdStat = [fltrd[i] for i in ['kassist', 'death']]
COLORS = ['#1A1AAE99', '#C12D7499']
ZORDER = [0, 2]
mult = [1, 1]
(fig, ax) = plt.subplots(figsize=(20, 3))
for (ix, st) in enumerate(fltrdStat):
    kFreqs = mult[ix]*splat.calcBinnedFrequencies(st, xRan[0], xRan[1], normalized=True)
    for (x, k) in enumerate(kFreqs):
        ax.add_patch(
            Rectangle(
                (x, 0), binSize, k, 
                facecolor=COLORS[ix], edgecolor='#000000',
                zorder=ZORDER[ix]
                # alpha=alpha, zorder=0, **kwargs
            )
        )
ax.set_xlim(*xRan)
ax.set_ylim(0, .25)



sns.stripplot(
    data=dfStats[dfStats['weapon']==wpn], x="kill",
    jitter=0.1,
    size=0.5, alpha=0.05
)
sns.violinplot(list(dfStats[dfStats['weapon']==wpn]['kill']))