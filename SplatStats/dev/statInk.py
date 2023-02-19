
# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

import re
from os import path
from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import radians, log10
from matplotlib import colors
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import SplatStats as splat
import chord as chd

DATA_PATH = '/Users/sanchez.hmsc/Documents/SyncMega/BattlesDocker/battle-results-csv'
FPATHS = glob(path.join(DATA_PATH, '*-*-*.csv'))

###############################################################################
# Read Full Data
###############################################################################
DFS_LIST = [pd.read_csv(f, dtype=splat.STATINK_DTYPES, parse_dates=['period']) for f in FPATHS]
FULL_DF = pd.concat(DFS_LIST)
cols = [i.replace('#', '').strip() for i in list(FULL_DF.columns)]
df = FULL_DF.copy()
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(DATA_PATH)
btls = statInk.battlesResults
###############################################################################
# Filter by Constraints
###############################################################################
fltrs = (
    btls['mode']=='Rainmaker',
    btls['season']=='Chill Season 2022'
)
fltrBool = [all(i) for i in zip(*fltrs)]
###############################################################################
# Frequency Analysis
###############################################################################
btlsFiltered = btls# [fltrBool]
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
# Calculating totals ----------------------------------------------------------
(totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
totalM = totalW + totalL
wpnsTriplets = zip(names, totalM, totalW, totalL)
wpnSortZip = zip(totalM, wpnsTriplets)
wpnsDict = {x[0]: (x[1], x[2], x[3]) for (_, x) in sorted(wpnSortZip)[::]}
wlRatio = [i[1]/i[0] for i in wpnsDict.values()]

labels = ['{} ({}%)'.format(n, int(f*100)) for (n, f) in zip(wpnsDict.keys(), wlRatio)]
(fig, ax) = plt.subplots(
    figsize=(12, 12), subplot_kw={"projection": "polar"}
)
(fig, ax) = splat.polarBarChart(
    labels, 
    [i[0] for i in wpnsDict.values()],
    yRange=(0, 1.5e6), rRange=(0, 270), ticksStep=15,
    colors=[c+'AA' for c in splat.ALL_COLORS],
    figAx=(fig, ax),
    ticksFmt={
        'lw': 2.5, 'range': (-.2, 1.5), 
        'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.1e}'
    },
    labelFmt={
        'color': '#000000EE', 'fontsize': 3, 
        'ha': 'left', 'fmt': '{:.1f}'
    }
)
(fig, ax) = splat.polarBarChart(
    labels, 
    [i[2] for i in wpnsDict.values()],
    yRange=(0, 1.5e6), rRange=(0, 270), ticksStep=15,
    figAx=(fig, ax),
    colors=[c+'FF' for c in splat.ALL_COLORS],
    ticksFmt={
        'lw': 2.5, 'range': (-.2, 1.5), 
        'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.1e}'
    },
    labelFmt={
        'color': '#000000EE', 'fontsize': 3, 
        'ha': 'left', 'fmt': '{:.1f}'
    }
)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=5)
fName = 'Polar.png'
plt.savefig(
    path.join('/Users/sanchez.hmsc/Desktop', fName),
    dpi=300, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')




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

