# !/usr/bin/env python3

import os    
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import numpy as np
from os import path
from sys import argv
from glob import glob
from random import shuffle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import SplatStats as splat


if splat.isNotebook():
    (SEASON, GMODE, TITLES, OVERWRITE, DPI) = (
        'Drizzle Season 2022', 'All Modes', 'False', 'True', '500'
    )
else:
    (SEASON, GMODE, TITLES, OVERWRITE, DPI) = argv[1:]
dpi = int(DPI)
overwrite = (True if OVERWRITE=="True"  else False)
titles = (True if TITLES=="True"  else False)
prepFnme = ('' if titles else 'Untitled_')
###############################################################################
# Constants
###############################################################################
GMODES = {'Clam Blitz', 'Splat Zones', 'Tower Control', 'Turf War', 'Rainmaker'}
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
    DATA_PATH = '/Users/sanchez.hmsc/Documents/BattlesDocker/'
    splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
else:
    DATA_PATH = '/data/'
    splat.setSplatoonFont('/other/', fontName="Splatfont 2")
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
COLORS = splat.ALL_COLORS
shuffle(COLORS)
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
try:
    six = list(set(btls['season'])).index(SEASON)
    FREQ_SCALER = 1
except:
    six = -1
    SEASON = 'All Seasons'
    FREQ_SCALER = 4
POLAR['yRange'] = (POLAR['yRange'][0], POLAR['yRange'][1]*FREQ_SCALER)
FNSTR = '{} ({}) - '.format(SEASON, GMODE)
if SEASON!='All Seasons':
    if GMODE in GMODES:
        fltrs = (btls['season']==SEASON, btls['mode']==GMODE)
        fltrBool = [all(i) for i in zip(*fltrs)]
        btlsFiltered = btls[fltrBool]
    else:
        GMODE = 'All'
        fltrs = (btls['season']==SEASON, )
        fltrBool = [all(i) for i in zip(*fltrs)]
        btlsFiltered = btls[fltrBool]
else:
    if GMODE in GMODES:
        fltrs = (btls['mode']==GMODE, )
        fltrBool = [all(i) for i in zip(*fltrs)]
        btlsFiltered = btls[fltrBool]
    else:
        btlsFiltered = btls
###############################################################################
# Get Weapon use Stats
###############################################################################
def addDateGroup(
        playerHistory, 
        slicer=(lambda x: "{}/{:02d}".format(
            x.isocalendar().year, x.isocalendar().week
        )),
        dateColumn='datetime'
    ):
    dteSlice = playerHistory[dateColumn].apply(slicer).copy()
    playerHistory.insert(3, 'DateGroup', dteSlice)
    return playerHistory        

LABELS = ('kill', 'kill-assist', 'assist', 'death', 'inked')
PLAYERS = ('A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4')
        
slicer = (lambda x: "{}/{:02d}/{}".format(
    x.isocalendar().year, x.isocalendar().week, x.day
))
addDateGroup(btlsFiltered, slicer=slicer, dateColumn='period')
wpnsSet = splat.getWeaponsSet(btlsFiltered)


dfs = []
for plyNme in PLAYERS:
    plyLbs = {f'{plyNme}-{c}': c for c in LABELS}
    fltr = btlsFiltered.groupby([f'{plyNme}-weapon', 'DateGroup']).sum('kill')[
        plyLbs.keys()
    ]
    fltr.rename(plyLbs, axis='columns', inplace=True)
    fltr.index.names = ['main weapon', 'DateGroup']
    dfs.append(fltr)
grpd = pd.concat(dfs)
grpd.replace([np.inf, np.nan, -np.inf], 0, inplace=True)
pivot = grpd.reset_index().pivot_table(
    values=LABELS, index=['main weapon', 'DateGroup'], aggfunc='sum'
)
tCardsDict = {cat: pivot[cat] for cat in LABELS}

tCard = tCardsDict['kill']

wpnSorting = tCard.sum(axis=1).sort_values(ascending=False)
wpnsNumber = len(wpnSorting)
fontSize = np.interp(wpnsNumber, [1, 10, 30, 50], [30, 20, 14, 5])
(fig, ax) = splat.plotTimecard(
    tCard, wpnSorting, 
    fontSize=fontSize, 
    fmtStr='  {} ({:.0f})', statScaler=60,
    highColors=['#DE0B64AA', '#311AA8AA', '#6BFF00AA', '#9030FFAA', '#B62EA7AA']
)



# grpdDF = [
#     btlsFiltered.groupby([f'{plyr}-weapon', 'DateGroup']).sum('kill')
#     for plyr in ('A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4')
# ]
# for (ix, plyr) in enumerate(('A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4')):
#     grpdDF[ix].index.names = ['main weapon', 'DateGroup']
# grpd = pd.concat(grpdDF)
# # grpd['kad'] = grpd['kassist']/grpd['death']
# grpd.replace([np.inf, np.nan, -np.inf], 0, inplace=True)
# dfGroups = grpd.unstack().reset_index().set_index("main weapon")
# statsCats = sorted(list(set([i[0] for i in list(dfGroups.columns)])))
# tCardsDict = {cat: dfGroups[cat] for cat in statsCats}


