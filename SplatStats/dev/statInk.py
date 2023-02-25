
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
from colour import Color
from matplotlib.ticker import EngFormatter
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import SplatStats as splat
import chord as chd


USR='dsk'
season = 'Chill Season 2022'
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
###############################################################################
# Filter by Constraints
###############################################################################
fltrs = (
    # btls['mode']=='Turf War',
    btls['season']==season,
)
fltrBool = [all(i) for i in zip(*fltrs)]
btlsFiltered = btls[fltrBool]
###############################################################################
# Frequency Analysis
###############################################################################
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
# Calculating totals ----------------------------------------------------------
(totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
totalM = totalW + totalL
wpnsTriplets = zip(names, totalM, totalW, totalL)
wpnSortZip = zip(totalM, wpnsTriplets)
wpnsDict = {x[0]: (x[1], x[2], x[3]) for (_, x) in sorted(wpnSortZip)[::]}
wlRatio = [i[1]/i[0] for i in wpnsDict.values()]
# Polar barchart --------------------------------------------------------------
labels = ['{} ({}%)'.format(n, int(f*100)) for (n, f) in zip(wpnsDict.keys(), wlRatio)]
(fig, ax) = plt.subplots(
    figsize=(12, 12), subplot_kw={"projection": "polar"}
)
(fig, ax) = splat.polarBarChart(
    labels, [i[0] for i in wpnsDict.values()],
    yRange=(0, 1e6), rRange=(0, 180), ticksStep=4,
    colors=[c+'DD' for c in splat.ALL_COLORS],
    edgecolor='#00000088', linewidth=0,
    figAx=(fig, ax),
    ticksFmt={
        'lw': 1, 'range': (-.2, 1), 
        'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.1e}'
    },
    labelFmt={
        'color': '#000000EE', 'fontsize': 4.25, 
        'ha': 'left', 'fmt': '{:.1f}'
    }
)
# formatter1 = EngFormatter(places=1, unit="", sep="")
# ax.xaxis.set_major_formatter(formatter1)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=7.5)
fName = 'Polar - {}.png'.format(season)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Frequency Analysis
###############################################################################
cntr = Counter(btlsFiltered['lobby'])
# Generate lobby barchart -----------------------------------------------------
(fig, ax) = plt.subplots(figsize=(0.4, 20))
(series, data) = (list(cntr.keys()), [[int(i)] for i in list(cntr.values())])
(fig, ax) = splat.plotStackedBar(
    data, series, 
    labels=[i.replace(' ', '\n') for i in list(cntr.keys())],
    figAx=(fig, ax),
    category_labels=False, 
    show_values=True, 
    value_format="{:.0f}",
    colors=[
        '#413BBA', '#C83D79', '#8ED11E', '#FDFF00', '#03C1CD', '#C70864'
    ],
    fontsize=8.5, xTickOffset=0.7
)
ax.axis('off')
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.text(
    -2.25, 0.5, 'Total matches: {}'.format(np.sum(data)),
    fontsize=25,
    horizontalalignment='center',
    verticalalignment='center',
    transform=ax.transAxes,
    rotation=90
)
fName = 'StackedLobby - {}.png'.format(season)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')
