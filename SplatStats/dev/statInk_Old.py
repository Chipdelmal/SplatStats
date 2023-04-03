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
    # dfs.append(df.groupby(['weapon']).sum())
    dfs.append(df)
# statsDF = sum(dfs)
# statsDF['kassist'] = statsDF['kill']+statsDF['assist']/2
# meanable = ['kill', 'assist', 'death', 'inked', 'special', 'kassist']
dfStats = pd.concat(dfs)
weapons = sorted(list(dfStats['weapon'].unique()))
wpn = weapons[0]

xRan = (0, 50)
fltrd = dfStats[dfStats['weapon']==wpn]['kill']
splat.calcBinnedFrequencies(fltrd, xRan[0], xRan[1])


sns.stripplot(
    data=dfStats[dfStats['weapon']==wpn], x="kill",
    jitter=0.1,
    size=0.5, alpha=0.05
)
sns.violinplot(list(dfStats[dfStats['weapon']==wpn]['kill']))