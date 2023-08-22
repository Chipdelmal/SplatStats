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
dfStats['kassist'] = dfStats['kill']+dfStats['assist']/2
dfStats['paint'] = dfStats['inked']/100

stats = ['kill', 'death', 'assist', 'special', 'paint']
wpnHists = splat.getWeaponsStatsHistograms(
    dfStats, weapons, (0, 30), binSize=1, stats=stats
)
wpnMeans = splat.getWeaponsStatsSummary(
    dfStats, weapons, summaryFunction=np.mean, stats=stats
)
stat = 'death'
statPars = splat.INKSTATS_STYLE[stat]
(fig, ax) = splat.plotWeaponsStrips(
    wpnHists, weapons, stat,
    figAx=None,
    weaponsSummary=wpnMeans,
    color=statPars['color'], range=statPars['range'],
    cScaler=statPars['scaler'],
    binSize=1
)
