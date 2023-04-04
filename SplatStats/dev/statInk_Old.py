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
from matplotlib.patches import Rectangle


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
btlsFiltered['matches'] = [1]*btlsFiltered.shape[0]
###############################################################################
# Frequency Analysis
###############################################################################
prepend = 'A1'
dfs = []
for prepend in ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']:
    cols = ['weapon', 'kill', 'assist', 'death', 'inked', 'special']
    df = btlsFiltered[[prepend+'-{}'.format(c) for c in cols]+['matches']]
    df.columns = [c[3:] for c in df.columns[:-1]]+['matches']
    dfs.append(df)
dfStats = pd.concat(dfs)
dfStats['kassist'] = dfStats['kill']+dfStats['assist']/2
dfStats['paint'] = dfStats['inked']/100
weapons = sorted(list(dfStats['weapon'].unique()))


STATS = {
    'stat': ['kill', 'death', 'assist', 'special', 'paint'],
    'colors': ['#1A1AAEDD', '#C12D74DD', '#35BA49DD', '#801AB3DD', '#EE8711DD']
}
STATS['cmaps'] = [
    splat.colorPaletteFromHexList(['#ffffff00', c]) for c in STATS['colors']
]


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
                facecolor=STATS['cmaps'][ix](k*10), edgecolor='#000000',
            )
        )
ax.set_title(wpn)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xlim(*xRan)
ax.set_ylim(0, len(STATS['stat']))









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