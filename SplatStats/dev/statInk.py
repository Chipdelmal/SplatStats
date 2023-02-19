
# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

import re
from os import path
from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from sklearn.feature_extraction import DictVectorizer
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
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
# Demo Analysis
###############################################################################
fltrs = (
    btls['mode']=='Rainmaker',
    btls['season']=='Chill Season 2022'
)
fltrBool = [all(i) for i in zip(*fltrs)]

btlsFiltered = btls[fltrBool]
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
sums = np.sum(matrix, axis=1)

selfProb = np.diag(matrix.copy(), k=0)
norm = colors.Normalize(vmin=np.min(matrix), vmax=np.max(matrix))
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
# Testing class
###############################################################################
plt.matshow(matrix)
