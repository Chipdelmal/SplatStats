# !/usr/bin/env python3

# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

from os import path
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from colour import Color
from matplotlib.ticker import EngFormatter
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import SplatStats as splat
import chord as chd
import matplotlib.colors as colors
from scipy.stats import entropy

(six, USR) = (2, 'dsk')
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
# for gmode in ('Tower Control', 'Splat Zones', 'Turf War', 'Clam Blitz', 'Rainmaker'):
fltrs = (btls['season']==SEASON, ) # btls['mode']==gmode)
fltrBool = [all(i) for i in zip(*fltrs)]
btlsFiltered = btls[fltrBool]
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
tauW = np.zeros((len(matrix), len(matrix)))
for (ix, wp) in enumerate(names):
    winsDiff = matrix[ix]/matrix[:,ix]
    tauW[ix] = winsDiff
(totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
totalM = totalW + totalL
###############################################################################
# Matrices
###############################################################################
(TITLE, RAN) = (True, 0.75)
COLS = (
    ('#B400FF', '#1D07AC'), ('#D01D79', '#1D07AC'), ('#6BFF00', '#1D07AC')
)
# Re-Arrange Stuff ------------------------------------------------------------
tauX = np.copy(tauW)-1
sorting = list(np.argsort([np.sum(r>0) for r in tauX]))[::-1]
# sorting = list(np.argsort([np.sum(r) for r in tauX]))[::-1]
tauS = tauX[sorting][:,sorting]
namS = [names[i] for i in sorting]
counts = [np.sum(r>0) for r in tauS]
(tot, mns, sds) = (
    np.sum(tauS, axis=1), np.mean(tauS, axis=1), np.std(tauS, axis=1)
)
totMat = totalM[sorting]
lLabs = ['{} ({})'.format(n, c) for (n, c) in zip(namS, counts)]
tLabs = ['({:03d}k) {}'.format(c, n) for (n, c) in zip(namS, [int(i) for i in totMat/1e3])]
# rLabs = ['{:02d} ({:03d}k)'.format(t, s) for (t, s) in zip(counts, [int(i) for i in totMat/1e3])]
pal = splat.colorPaletteFromHexList([COLS[six][0], '#FFFFFF', COLS[six][1]])
(fig, ax) = plt.subplots(figsize=(20, 20))
im = ax.matshow(tauS, vmin=-RAN, vmax=RAN, cmap=pal)
ax.set_xticks(np.arange(0, len(namS)))
ax.set_yticks(np.arange(0, len(namS)))
ax.set_xticklabels(tLabs, rotation=90, fontsize=12.5)
ax.set_yticklabels(lLabs, fontsize=12.5)
yLims = ax.get_ylim()
# ax2 = ax.twinx()
# ax2 = fig.add_subplot(111, sharex=ax, frameon=False)
# ax2.matshow(tauS, vmin=-RAN, vmax=RAN, cmap=pal)
# ax2.yaxis.tick_right()
# ax2.set_ylim(*yLims)
# ax2.set_xticks(np.arange(0, len(namS)))
# ax2.set_xticklabels(namS, rotation=90, fontsize=12.5)
# ax2.set_yticks(np.arange(0, len(namS)))
# ax2.set_yticklabels(rLabs, fontsize=12.5)
# fig.colorbar(im, ax=ax, orientation="horizontal", pad=0.2)
if TITLE:
    ax.set_title(SEASON, fontsize=50, y=-.06)
fName = '{} Weapon Matrix.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')


