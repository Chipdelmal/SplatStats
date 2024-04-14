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
        
slicer = (lambda x: "{}/{:02d}".format(
    x.isocalendar().year, x.isocalendar().week
))
addDateGroup(btlsFiltered, slicer=slicer, dateColumn='period')
wpnsSet = splat.getWeaponsSet(btlsFiltered)
###############################################################################
# Get Season Dates
###############################################################################
seasons = list(set(btls['season']))
seasonDtes = dict()
seasonLsts = []
for ssn in seasons:
    dtesSet = set(btls[btls['season']==ssn]['DateGroup'])
    dteRange = (min(dtesSet), max(dtesSet))
    seasonDtes[ssn] = dteRange
    seasonLsts.append(ssn)
###############################################################################
# Get Version Dates
###############################################################################
versions = sorted(list(set(btls['game-ver'])))
versionDtes = dict()
for vrs in versions[:-1]:
    dtesSet = set(btls[btls['game-ver']==vrs]['DateGroup'])
    dteRange = (min(dtesSet), max(dtesSet))
    versionDtes[vrs] = dteRange
###############################################################################
# Get Splatfest
###############################################################################
fest = sorted(list(set(btls[btls['lobby']=='Splatfest (Open)']['DateGroup'])))
fix = fest[0]
flag = False
fDates = []
for (ix, fix) in enumerate(fest):
    if ix < (len(fest)-1):
        cfix = int(fest[ix].split('/')[1])
        ffix = int(fest[ix+1].split('/')[1])
        if flag:
            flag = False
        else:
            if ffix == cfix+1:
                flag = True
            else:
                flag = False
            fDates.append(fest[ix])
    else:
        fDates.append(fest[ix])

dfs = []
for plyNme in PLAYERS:
    plyLbs = {f'{plyNme}-{c}': c for c in LABELS}
    plyLbs['time'] = 'time'
    fltr = btlsFiltered.groupby([f'{plyNme}-weapon', 'DateGroup']).sum('kill')[
        plyLbs.keys()
    ]
    fltr.rename(plyLbs, axis='columns', inplace=True)
    fltr.index.names = ['main weapon', 'DateGroup']
    dfs.append(fltr)
grpd = pd.concat(dfs)
grpd.replace([np.inf, np.nan, -np.inf], 0, inplace=True)
pivot = grpd.reset_index().pivot_table(
    values=list(LABELS)+['time'], 
    index=['main weapon', 'DateGroup'], 
    aggfunc='sum'
)
tCardsDict = {cat: pivot[cat].unstack() for cat in list(LABELS)+['time']}
[
    tCardsDict[c].replace([np.inf, np.nan, -np.inf], 0, inplace=True) 
    for c in LABELS
]



stat = 'time'
tCard = tCardsDict[stat]

wpnSorting = tCard.sum(axis=1).sort_values(ascending=False)
wpnsNumber = len(wpnSorting)
fontSize = np.interp(wpnsNumber, [1, 10, 30, 50], [30, 18, 12, 3])
# (fig, ax) = splat.plotTimecard(
#     tCard, wpnSorting, 
#     fontSize=fontSize, 
#     fmtStr='  {} ({:.0f})', statScaler=60,
#     highColors=['#DE0B64AA', '#311AA8AA', '#6BFF00AA', '#9030FFAA', '#B62EA7AA']
# )


timecard=tCard
wpnSorting=wpnSorting


figAx=None
yearRange=None
weekRange=None
reversed=False
origin='N'
direction=1
rRange=(0, 90)
offset=0
height=1
edgeWidth=0.1
fontSize=np.interp(wpnsNumber, [1, 10, 30, 50], [30, 20, 12, 4])
highColors=[
    '#DE0B64FF', '#311AA8FF', '#6BFF00FF', '#9030FFFF', 
    '#B62EA7FF', '#7d8597FF', '#faa6ffFF', '#f4845fFF'
]
baseColor='#00000066'
maxValue=None
fmtStr='  {}'
statScaler=1
normalized=True
# normFunction=LogNorm
normFunction=lambda x: np.interp(x, [0, maxMag], [0, 1], left=None)
normFunction=PowerNorm(gamma=1/2, vmin=0, vmax=1)
normFunction=SymLogNorm(1e7/5, vmin=0, vmax=1e7/1.5)
# normFunction=SymLogNorm(3e5/5, vmin=0, vmax=3e5/1.5)

wpnsNumber = len(wpnSorting)
cmaps = [splat.colorPaletteFromHexList([baseColor, c]) for c in highColors]
if normalized:
    timecard = timecard# /timecard.sum(axis=0)
if not maxValue:
    maxMag = max(timecard.max())
    # norm = LogNorm(vmin=1, vmax=maxMag)
    # norm = lambda x: np.interp(x, [0, maxMag/5], [0, 1], left=None)
    norm = normFunction# PowerNorm(gamma=1/2, vmin=0, vmax=maxMag)
else:
    norm = LogNorm(vmin=1, vmax=maxValue)
if (yearRange is None) or (weekRange is None):
    (minDate, maxDate) = (
        sorted(timecard.columns)[0], 
        sorted(timecard.columns)[-1]
    )
    (minYear, minWeek) = (int(minDate[:4]), int(minDate[5:]))
    (maxYear, maxWeek) = (int(maxDate[:4]), int(maxDate[5:]))
else:
    (minYear, maxYear) = yearRange
    (minWeek, maxWeek) = weekRange
# Plot --------------------------------------------------------------------
if not figAx:
    (fig, ax) = plt.subplots(
        figsize=(10, 10),  subplot_kw={"projection": "polar"}
    )
for wpix in range(wpnsNumber):
    (wpnCurrent, wpnTotal) = (
        wpnSorting.index[::-1][wpix], 
        wpnSorting.values[::-1][wpix]
    )
    wpnLabel = fmtStr.format(wpnCurrent, wpnTotal/statScaler)
    cmapCurrent = cmaps[wpix%len(cmaps)]
    # Get weapon values and dates -----------------------------------------
    rowValues = timecard.loc[wpnCurrent]
    if not reversed:
        (rowDates, rowMagnitudes) = (
            list(rowValues.index)[::-1], 
            list(rowValues.values)[::-1]
        )
    else:
        (rowDates, rowMagnitudes) = (
            list(rowValues.index), 
            list(rowValues.values)
        )
    # Convert dates to x coordinates --------------------------------------
    dateTuples = [[int(x) for x in d.split('/')] for d in rowDates]
    weekNumber = [(y%minYear)*52+w-minWeek+1 for (y, w) in dateTuples]
    # Convert values to colors --------------------------------------------
    rDelta = radians(rRange[1])/len(weekNumber)
    deltas = np.arange(0, radians(rRange[1])+rDelta, rDelta)
    weekBars = [(i*rDelta, rDelta) for i in range(len(deltas)-1)]
    clrsBlocks = [cmapCurrent(norm(value)) for value in rowMagnitudes]
    ax.broken_barh(
        weekBars, (offset+wpix*height, height), lw=edgeWidth,
        facecolors=clrsBlocks, edgecolors='#ffffff44'
    )
    ax.text(
        0, # deltas[-1], 
        offset+wpix*height+height/2, wpnLabel,
        va='center', ha='left', fontsize=fontSize,
        color='#ffffffDD'
    )
maxWeek = max(weekNumber)
# Plot version ----------------------------------------------------------------
# verTuples = [(k, versionDtes[k][0]) for k in versionDtes.keys()]
# (verLbl, verDte) = list(zip(*verTuples))
# dteTuples = [[int(x) for x in d.split('/')] for d in verDte]
# weekNumber = [(y%minYear)*52+w-minWeek+1 for (y, w) in dteTuples]
# # wix = weekNumber[10]
# for wix in weekNumber:
#     ax.plot(
#         [0, weekBars[-wix][0]+rDelta], 
#         [0, wpnsNumber+0], 
#         alpha=0.25,
#         color='#bdd5ea', 
#         lw=1, ls=(0, (1, 10)),
#         zorder=20
#     )
# Plot splatfest --------------------------------------------------------------
dteTuples = [[int(x) for x in d.split('/')] for d in fDates]
weekNumber = [(y%minYear)*52+w-minWeek+1 for (y, w) in dteTuples]
# wix = weekNumber[0]
for wix in weekNumber:
    ax.plot(
        [0, weekBars[-wix][0]+rDelta], 
        [0, wpnsNumber], 
        alpha=0.25,
        color='#bdd5ea', 
        lw=1, # ls=(0, (10, 5)),
        zorder=10
    )
# Plot season ----------------------------------------------------------------
ssnTuples = [(k, seasonDtes[k][0]) for k in seasonDtes.keys()]
(ssnLbl, ssnDte) = list(zip(*ssnTuples))
dteTuples = [[int(x) for x in d.split('/')] for d in ssnDte]
weekNumber = [(y%minYear)*52+w-minWeek+1 for (y, w) in dteTuples]
# wix = weekNumber[0]
ix = 0
for wix in weekNumber:
    ax.plot(
        [0, weekBars[-wix][0]+rDelta], 
        [0, wpnsNumber], 
        alpha=0.75, lw=1.25, 
        color='#C1D0F9', 
        zorder=10
    )
    ax.text(
        weekBars[-wix][0]-rDelta*0.5+rDelta,
        wpnsNumber+4, 
        '{} ({})      '.format(seasonLsts[ix][:-12], seasonLsts[ix][-2:]),
        va='center', ha='center', fontsize=fontSize*2,
        color='#ffffffDD', 
        rotation=np.interp(wix, [0, maxWeek], [0, -90])
    )
    ix = ix + 1 
ax.text(
    0.5, -0.025, f'Weapon usage (binned by week)', # \nby {stat}',
    va='top', ha='center', rotation=0,
    transform=ax.transAxes, fontsize=fontSize*6,
    color='#ffffffDD'
)
# ax.set_xticks()
# ax.set_xticklabels()
ax.set_yticklabels([])
# ax.axis("off")
ax.set_thetamin(0)
ax.set_thetamax(rRange[1])
ax.set_ylim(0, offset+wpnsNumber*height+5)
ax.set_theta_zero_location(origin)
ax.set_theta_direction(direction)
ax.spines['polar'].set_visible(False)
ax.set_rlabel_position(0)
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_facecolor("#000000")
plt.figure(facecolor="#000000")
fig.patch.set_facecolor("#000000")
fName = f'Timecard-{stat}.png'
fig.savefig(
    path.join(DATA_PATH, 'inkstats/'+fName), 
    dpi=350, bbox_inches='tight', facecolor=fig.get_facecolor()
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