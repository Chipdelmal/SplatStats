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
from math import radians, sin, cos
from matplotlib.colors import LogNorm, PowerNorm, SymLogNorm
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from collections import Counter, OrderedDict
import SplatStats as splat


if splat.isNotebook():
    (SEASON, GMODE, TITLES, OVERWRITE, DPI) = (
        'All', 'All Modes', 'False', 'True', '500'
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
    DATA_PATH = '/Users/chipdelmal/Documents/BattlesDocker/'
    splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
else:
    DATA_PATH = '/data/'
    splat.setSplatoonFont('/other/', fontName="Splatfont 2")
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
COLORS = splat.ALL_COLORS
shuffle(COLORS)
###############################################################################
# Parse and Filter Data Object
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
# Add 'day' to dataset for filtering ------------------------------------------
dfBtls = btlsFiltered.copy()
dfBtls['day'] = dfBtls['period'].dt.floor('d')
UNIQUE_DAYS = sorted(btlsFiltered['day'].unique())
###############################################################################
# Aggregate
###############################################################################       
LABELS = ('kill', 'kill-assist', 'assist', 'death', 'inked')
PLAYERS = ('A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4')
IDS = [f'{p}-weapon' for p in PLAYERS]
# Count weapons everyday ------------------------------------------------------
(ctsDict, fullCtr, wpnsSet) = (OrderedDict(), Counter(), set())
for day in UNIQUE_DAYS:
    dayBtls = dfBtls[dfBtls['day']==day]
    dayCtrs = [Counter(dayBtls[p]) for p in IDS]
    dayWpns = sum(dayCtrs, Counter())
    fullCtr = sum([fullCtr, dayWpns], Counter())
    ctsDict[day] = dayWpns
    wpnsSet.update(set(dayWpns.keys()))
(WPNS_FREQ, WPNS_TOTAL, WPNS_LIST) = (ctsDict, fullCtr, sorted(list(wpnsSet)))
###############################################################################
# Assemble dataframe
###############################################################################  
WPNS_FREQ_DF = pd.DataFrame.from_records(
    list(WPNS_FREQ.values()), columns=WPNS_LIST, index=UNIQUE_DAYS
).fillna(0).astype(int)
###############################################################################
# Get Splatfest
###############################################################################  
(seasons, versions) = (
    list(dfBtls['season'].unique()),
    sorted(list(dfBtls['game-ver'].unique()))
)
(SESONS_START, VERSIONS_START) = (
    {s: min(dfBtls[dfBtls['season']==s]['day']) for s in seasons},
    {s: min(dfBtls[dfBtls['game-ver']==s]['day']) for s in versions}
)
SPLATFEST_DAYS = sorted(list(
    dfBtls[
        (dfBtls['lobby']=='Splatfest (Open)') |
        (dfBtls['lobby']=='Splatfest (Pro)')
    ]['day'].unique()
))