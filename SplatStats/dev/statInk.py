# !/usr/bin/env python3

import numpy as np
from os import path
from sys import argv
from glob import glob
from random import shuffle
import matplotlib.pyplot as plt
import SplatStats as splat
from datetime import datetime


if splat.isNotebook():
    (six, USR) = (2, 'lap')
    GMODE = 'Rainmaker'
    SSN_TITLE = True
else:
    (six, GMODE, ssn) = argv[1:]
    six = int(six)
    SSN_TITLE = int(ssn)
DPI=300
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
    if USR=='lab':
        DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
    elif USR=='lap':
        DATA_PATH = '/Users/sanchez.hmsc/Documents/BattlesDocker/'
    else:
        DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
else:
    DATA_PATH = '/Users/sanchez.hmsc/Documents/BattlesDocker/'
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
COLORS = splat.ALL_COLORS
shuffle(COLORS)
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
###############################################################################
# Filter by Constraints
###############################################################################
try:
    SEASON = list(btls['season'].unique())[six]
    FREQ_SCALER = 1
except:
    SEASON = 'All Seasons'
    FREQ_SCALER = 2
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
# Get Total Season Frequencies and Dominance Matrix
###############################################################################
(wpnFreq, wpnWLT, lbyFreq, lbyDaily) = (
    splat.getWeaponsFrequencies(btlsFiltered),
    splat.getWeaponsWLT(btlsFiltered),
    splat.getLobbyFrequencies(btlsFiltered),
    splat.countDailyLobbies(btlsFiltered)
)
lbyGaussDaily = splat.smoothCountDailyLobbies(lbyDaily)
(mNames, mMatrix) = splat.calculateDominanceMatrix(btlsFiltered)
(sNames, sMatrix, sSort) = splat.normalizeDominanceMatrix(mNames, mMatrix)
# Calculate auxiliary metrics -------------------------------------------------
wpnRank = splat.rankWeaponsFrequency(wpnFreq, wpnWLT)
(mWpnWins, mWpnLoss) = (
    np.sum(mMatrix, axis=1)/4, 
    np.sum(mMatrix, axis=0)/4
)
period = (min(btlsFiltered['period']), max(btlsFiltered['period']))
# Checks for consistency ------------------------------------------------------
tests = [
    np.sum(list(wpnFreq.values()))/8 == btlsFiltered.shape[0],
    np.sum(list(lbyFreq.values()))   == btlsFiltered.shape[0],
    np.sum(np.sum(wpnWLT[1][:,2]))   == np.sum(list(wpnFreq.values())),
    all(mWpnWins == wpnWLT[1][:,0]),
    all(mWpnLoss == wpnWLT[1][:,1]),
    all(wpnWLT[1][:,2] == mWpnWins+mWpnLoss)
]
assert(all(tests))
###############################################################################
# Get Frequencies for Strips
###############################################################################
dfStats = splat.getWeaponsDataframe(btlsFiltered)
weapons = sorted(list(dfStats['weapon'].unique()))
dfStats['kassist'] = dfStats['kill']+dfStats['assist']/2
dfStats['paint'] = dfStats['inked']/100
wpnStats = ['kill', 'death', 'assist', 'special', 'paint']
wpnHists = splat.getWeaponsStatsHistograms(
    dfStats, weapons, (0, 30), binSize=1, stats=wpnStats
)
wpnMeans = splat.getWeaponsStatsSummary(
    dfStats, weapons, summaryFunction=np.mean, stats=wpnStats
)
###########################################################################
# Weapon Matrix
###########################################################################
fName = FNSTR+'Matrix.png'
COLS = splat.SEASON_COLORS
cPal = splat.colorPaletteFromHexList([COLS[six][0]+'DD', '#FFFFFF99', COLS[six][1]+'DD'])
(fig, ax) = plt.subplots(figsize=(20, 20))
(fig, ax) = splat.plotDominanceMatrix(
    sNames, sMatrix, sSort, mMatrix,
    figAx=(fig, ax), vRange=(-0.75, 0.75), cmap=cPal
)
plt.tick_params(
    axis='x', which='both',
    bottom=False, top=True, labelbottom=False
)
if SSN_TITLE:
    fName = FNSTR+'Matrix_S.png'
    ax.set_title(
        '{}\n({} matches from {} to {})'.format(
            SEASON, btlsFiltered.shape[0],
            period[0].strftime("%b %d"), 
            period[1].strftime("%b %d")
        )
        , fontsize=35, y=-.085
    )
    (transp, fc) = (False, '#ffffff')
else:
    ax.set_title(
        'Matches: {}'.format(btlsFiltered.shape[0])
        , fontsize=35, y=-.045
    )
    (transp, fc) = (True, '#ffffff00')
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=DPI, transparent=transp, facecolor=fc, bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Plot Total Frequencies
###############################################################################
fName = FNSTR+'Polar.png'
if GMODE in GMODES:
    POLAR['topRank'] = (len(wpnRank)-20, len(wpnRank))
if SSN_TITLE:
    fName = FNSTR+'Polar_S.png'
    POLAR['rRange'] = (0, 90)
    POLAR['ticksStep'] = 2
(fig, ax) = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})
(fig, ax) = splat.plotPolarFrequencies(
    wpnFreq, wpnRank, figAx=(fig, ax),
    fontSizes=POLAR['fontSizes'], ticksStep=POLAR['ticksStep'],
    yRange=POLAR['yRange'], rRange=POLAR['rRange'],
    topRank=POLAR['topRank']
)
if TITLES and not SSN_TITLE:
    partp = np.sum(list(wpnFreq.values()))
    if GMODE in GMODES:
        fstr = '{} ({:.0f}{})'.format(GMODE, partp/PART_SCALER[1], PART_SCALER[0])
    else:
        fstr = 'Participation: {:.2f}{}'.format(partp/PART_SCALER[1], PART_SCALER[0])
    ax.text(
        0.5, 0.48, fstr,
        fontsize=20,
        horizontalalignment='right',
        verticalalignment='top',
        rotation=0,
        transform=ax.transAxes
    )
if SSN_TITLE:
    ax.set_title(SEASON, fontsize=35, y=0.5-.1, ha='right')
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=DPI, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Gaussian Lobby
###############################################################################
YLIM = (0, -1500)
if SEASON=='All Seasons':
    YLIM = (0, -3500)
if GMODE not in GMODES:
    fName = FNSTR+'Mode.png'
    (fig, ax) = (plt.figure(figsize=(20, 3)), plt.axes())
    (fig, ax) = splat.plotGaussianLobby(
        lbyDaily, lbyGaussDaily, figAx=(fig, ax), ylim=YLIM
    )
    ax.set_ylim(*YLIM)
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.savefig(
        path.join(DATA_PATH, 'statInk/'+fName),
        dpi=DPI, transparent=False, facecolor='#ffffff', bbox_inches='tight'
    )
    plt.close('all')
###############################################################################
# Lobby Type
###############################################################################
if GMODE not in GMODES:
    fName = FNSTR+'Lobby.png'
    (fig, ax) = plt.subplots(figsize=(0.4, 20))
    (fig, ax) = splat.barChartLobby(lbyFreq)
    plt.savefig(
        path.join(DATA_PATH, 'statInk/'+fName), dpi=DPI, 
        transparent=False, facecolor='#ffffff', bbox_inches='tight'
    )
    plt.close('all')
###############################################################################
# Weapons Strips
###############################################################################
INKSTATS_STYLE = {
    'kill': {
        'color': '#1A1AAEDD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        'range': (0, 15)
    },
    'death': {
        'color': '#801AB3DD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        'range': (0, 15)
    },
    'assist': {
        'color': '#C12D74DD', 'range': (0, 10),
        'scaler': lambda x: np.interp(x, [0, 0.25, 0.65], [0, .70, 0.95]),
        
    },
    'special': {
        'color': '#1FAFE8DD', 'range': (0, 10),
        'scaler': lambda x: np.interp(x, [0, 0.25, 0.65], [0, .70, 0.95]),
    },
    'paint': {
        'color': '#35BA49DD', 'range': (0, 20),
        'scaler': lambda x: np.interp(x, [0, 0.1, 0.2], [0, .70, 0.95]),
    }
}
# (fig, axs) = plt.subplots(1, 5, figsize=(5*5, 20), sharey=True)
fName = FNSTR+'Strips.png'
fig = plt.figure(figsize=(5*5, 20))
gs = fig.add_gridspec(1, 5, hspace=1, wspace=0.05)
axs = gs.subplots()# sharex='col', sharey='row')
for (ix, stat) in enumerate(wpnStats):
    statPars = INKSTATS_STYLE[stat]
    (_, ax) = splat.plotWeaponsStrips(
        wpnHists, weapons, stat,
        figAx=(fig, axs[ix]),
        weaponsSummary=wpnMeans,
        color=statPars['color'], range=statPars['range'],
        cScaler=statPars['scaler']
    )
    axs[ix].xaxis.set_tick_params(labelsize=11)
    axs[ix].yaxis.set_tick_params(labelsize=11)
    axs[ix].yaxis.set_ticks_position('both')
    if (ix>0) and (ix<len(wpnStats)-1):
        axs[ix].set_yticklabels([])
    if ix == (len(wpnStats)-1):
        axs[ix].yaxis.tick_right()
        lbs = [i.get_text() for i in axs[0].get_yticklabels()]
        axs[ix].set_yticklabels(lbs)
        lbs = [int(i.get_text())*100 for i in axs[ix].get_xticklabels()]
        axs[ix].set_xticklabels(lbs)
        axs[ix].yaxis.set_ticks_position('both')
if SSN_TITLE:
    fName = FNSTR+'Strips_S.png'
    axs[2].text(
        0.5, 1.025, SEASON, 
        ha='center', va='bottom', 
        transform=axs[2].transAxes, fontsize=35
    )
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName), dpi=DPI, 
    transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')


# splat.plotWeaponStrip(
#         wpnHists, 'Splattershot', wpnStats,
#         figAx=plt.subplots(figsize=(20, 2)),
#         weaponsSummary=wpnMeans,
#         binSize=1
#     )
