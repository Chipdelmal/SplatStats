# !/usr/bin/env python3

# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

import fileinput
from os import path, system
from glob import glob
import pandas as pd
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
from colour import Color
from matplotlib.ticker import EngFormatter
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import SplatStats as splat
import chord as chd


USR='dsk'
# ['Drizzle Season 2022', 'Chill Season 2022', 'Fresh Season 2023']
SEASON = 'Fresh Season 2023'
TOP = 20
###############################################################################
# Get files and set font
###############################################################################
if USR=='lab':
    DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
else:
    DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
(names, matrix) = splat.calculateDominanceMatrixWins(btls)
ix = names.index("Splash-o-matic")
tups = [(names[i], matrix[ix, i]) for i in range(len(matrix))]
tups.sort(key = lambda x: x[1])
#
(totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
totalM = totalW + totalL
#
wmat = np.array([matrix[i]/totalM[i] for i in range(len(matrix))])
ix = names.index("Splash-o-matic")
tups = [(names[i], wmat[ix, i]) for i in range(len(wmat))]
tups.sort(key = lambda x: x[1])

wpnsTriplets = zip(names, totalM, totalW, totalL)
wpnSortZip = zip(totalM, wpnsTriplets)
wpnsDict = {x[0]: (x[1], x[2], x[3]) for (_, x) in sorted(wpnSortZip)[::]}
wlRatio = [i[1]/i[0] for i in wpnsDict.values()]


###############################################################################
# Chord Analysis
###############################################################################
btlsFiltered = btls[fltrBool]
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
sums = np.sum(matrix, axis=1)

selfProb = np.diag(matrix.copy(), k=0)
norm = colors.LogNorm(vmin=1, vmax=np.max(matrix))
colorPalette = splat.colorPaletteFromHexList(['#bdedf6', '#04067B'])
pColors = [colorPalette(norm(i)) for i in sums]

cMat = matrix.copy()
np.fill_diagonal(cMat, 0)

pad = 1.5
(fig, ax) = plt.subplots(figsize=(10, 10))
ax = chd.chord_modded(
    cMat, names, 
    ax=ax, rotate_names=[True]*len(names),
    fontcolor='k', chordwidth=.7, width=0.1, fontsize=4,
    extent=360, start_at=0,
    colors=pColors, use_gradient=True
)
ax.set_xlim(-pad, pad)
ax.set_ylim(-pad, pad)
ax.axis('off')
fName = 'Chord.png'
plt.savefig(
    path.join('/Users/sanchez.hmsc/Desktop', fName),
    dpi=300, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')

plt.matshow(matrix)


names[0]
sums = np.sum(matrix, axis=1)
(minIx, maxIx) = (
    np.where(sums==sums.min())[0][0],
    np.where(sums==sums.max())[0][0]
)
[names[i] for i in (minIx, maxIx)]

###############################################################################
# Aggregate by date
###############################################################################
df['dummy'] = [1]*df.shape[0]
counts = df.groupby([df['period'].dt.date]).count()['dummy']
(fig, ax) = (plt.figure(), plt.axes())
ax.plot(list(counts))
df['mode'] = [splat.GAME_MODE[lob] for lob in df['mode']]




###############################################################################
# Stacked by type
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
gmodes = zip(
    ['Turf War', 'Splat Zones', 'Tower Control', 'Rainmaker', 'Clam Blitz'],
    ['FF', '99', '77', '55', '44'],
    [.2, .4, .5, .6, .8]
)
###############################################################################
# Frequency Analysis
###############################################################################
btlsFiltered = btls
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
# Calculating totals ----------------------------------------------------------
(totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
totalM = totalW + totalL
wpnsTriplets = zip(names, totalM, totalW, totalL)
wpnSortZip = zip(totalM, wpnsTriplets)
wpnsDict = {x[0]: np.array([0, 0, 0]) for (_, x) in sorted(wpnSortZip)[::]}
# Generate figure -------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})
gm = 'Turf War'
lum = -.15
cols = splat.ALL_COLORS
for (gm, ap, lum) in gmodes:
    # lum = (lum + 0.15)
    ###########################################################################
    # Filter by Constraints
    ###########################################################################
    fltrs = (btls['mode']==gm,)
    fltrBool = [all(i) for i in zip(*fltrs)]
    btlsFiltered = btls[fltrBool]
    (names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
    (totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
    totalM = totalW + totalL
    for (ix, wpn) in enumerate(names):
        wpnsDict[wpn] = wpnsDict[wpn] + [totalM[ix], totalW[ix], totalL[ix]]

    colrs = []
    for c in splat.ALL_COLORS:
        cl = Color(c)
        cl.set_luminance(lum)
        colrs.append(cl.get_hex_l())

    (fig, ax) = splat.polarBarChart(
        wpnsDict.keys(), 
        [i[0] for i in wpnsDict.values()],
        figAx=(fig, ax),
        edgecolor='#00000088', linewidth=0.25,
        yRange=(0, 1.5e6), rRange=(0, 180), ticksStep=6,
        colors=[str(c)+ap for c in colrs],
        ticksFmt={
            'lw': 1, 'range': (-.2, 1), 
            'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.2e}'
        },
        labelFmt={
            'color': '#000000EE', 'fontsize': 4.25, 
            'ha': 'left', 'fmt': '{:.2f}'
        }
    )
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=7.5)
fName = 'PolarBroken.png'
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')


###############################################################################
# Win/Lose
###############################################################################
labels = ['{} ({}%)'.format(n, int(f*100)) for (n, f) in zip(wpnsDict.keys(), wlRatio)]
(fig, ax) = plt.subplots(
    figsize=(12, 12), subplot_kw={"projection": "polar"}
)
(fig, ax) = splat.polarBarChart(
    labels, 
    [i[0] for i in wpnsDict.values()],
    yRange=(0, 1.5e6), rRange=(0, 180), ticksStep=6,
    colors=[c+'DD' for c in splat.ALL_COLORS],
    edgecolor='#00000088', linewidth=0,
    figAx=(fig, ax),
    ticksFmt={
        'lw': 1, 'range': (-.2, 1), 
        'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.2e}'
    },
    labelFmt={
        'color': '#000000EE', 'fontsize': 4, 
        'ha': 'left', 'fmt': '{:.2f}'
    }
)
# (fig, ax) = splat.polarBarChart(
#     labels, 
#     [i[2] for i in wpnsDict.values()],
#     yRange=(0, 1.5e6), rRange=(0, 180), ticksStep=20,
#     figAx=(fig, ax),
#     colors=[c+'FF' for c in splat.ALL_COLORS],
#     edgecolor='#00000088', linewidth=0.25,
#     ticksFmt={
#         'lw': 1, 'range': (-.2, 1), 
#         'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.2e}'
#     },
#     labelFmt={
#         'color': '#000000EE', 'fontsize': 4.25, 
#         'ha': 'left', 'fmt': '{:.2f}'
#     }
# )
# formatter1 = EngFormatter(places=1, unit="", sep="")
# ax.xaxis.set_major_formatter(formatter1)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=7.5)
# ax.set_xlabel('Number [Hz]')
fName = 'Polar.png'
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')