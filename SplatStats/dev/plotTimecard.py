
import math
import numpy as np
from os import path
from sys import argv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import SplatStats as splat
from scipy import interpolate
from os import path
from matplotlib import colors
from math import radians, log10
import matplotlib.colors as mcolors
from collections import Counter
import warnings
warnings.filterwarnings("ignore")


if splat.isNotebook():
    (plyrName, weapon, mode, overwrite) = ('čħîþ ウナギ', 'All', 'All', 'False')
    (iPath, bPath, oPath) = (
        path.expanduser('~/Documents/BattlesDocker/jsons'),
        path.expanduser('~/Documents/BattlesDocker/battles'),
        path.expanduser('~/Documents/BattlesDocker/out')
    )
    fontPath = '~/Documents/BattlesDocker/'
else:
    (plyrName, weapon, mode, overwrite) = argv[1:]
    (iPath, bPath, oPath) = (
        '/data/jsons', 
        '/data/battles', 
        '/data/out'
    )
    fontPath = '/other/'
overwrite = (True if overwrite=="True"  else False)
LEN_LIMIT = 400
###############################################################################
# Auxiliary 
###############################################################################
fNameID = f'{plyrName}-{weapon}'
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=overwrite)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Player Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
playerHistory = playerHistory[playerHistory['match mode']!='PRIVATE']
# Weapon filter ---------------------------------------------------------------
if weapon != 'All':
    pHist = playerHistory[playerHistory['main weapon']==weapon]
else:
    pHist = playerHistory
    tCards = splat.getTimecard(playerHistory)
###############################################################################
# Strips
###############################################################################
STAT = 'duration'
tCard = tCards[STAT]
# Auxiliary variables --------------------------------------------------------
wpnSorting = tCard.sum(axis=1).sort_values(ascending=False)
wpnsNumber = len(wpnSorting)
fontSize = np.interp(wpnsNumber, [1, 10, 30, 50], [30, 20, 14, 5])
splat.plotTimecard(
    tCard, wpnSorting, 
    fontSize=fontSize, statScaler=60,
    highColors=['#DE0B64AA', '#311AA8AA', '#6BFF00AA', '#9030FFAA', '#B62EA7AA']
)

maxValue = max(dfCounts.max())
norm = colors.LogNorm(vmin=1, vmax=maxValue)

SAT_CATS = [
    '#311AA8AA', '#DE0B64AA', '#6BFF00AA', '#B62EA7AA', '#9030FF55',
]
MAPS = [splat.colorPaletteFromHexList(['#ffffff99', c]) for c in SAT_CATS]


wpnSorting = pHist.groupby('main weapon').sum(STAT)[STAT].sort_values(
    ascending=False
)


###############################################################################
# Polar Strips
###############################################################################
clockwise=True
rRange=(0, 90)
origin='N' 
direction=1
offset=0
height=1
double_label=False
wpnsNumber = len(wpnSorting)
fontSize = np.interp(wpnsNumber, [1, 10, 30, 50], [30, 20, 14, 5])

(fig, ax) = plt.subplots(
    figsize=(10, 10), subplot_kw={"projection": "polar"}
)
for wpix in range(wpnsNumber):
    (wpnCurrent, wpnTotal) = (
        wpnSorting.index[::-1][wpix],
        wpnSorting.values[::-1][wpix]
    )
    wpnLabel = f' {wpnCurrent} ({wpnTotal/60:.2f})'
    clr = MAPS[wpix%len(MAPS)]
    # Get weapon values and dates ------------------------------------------------
    rowValues = dfCounts.loc[wpnCurrent]
    (rowDates, rowMagnitudes) = (list(rowValues.index), list(rowValues.values))
    # Convert dates to x coordinates ---------------------------------------------
    dateTuples = [[int(x) for x in d.split('/')] for d in rowDates]
    weekNumber = [(y%minYear)*52+w-minWeek+1 for (y, w) in dateTuples]
    # Convert values to colors ---------------------------------------------------
    rDelta = radians(rRange[1])/weekNumber[-1]
    deltas = np.arange(0, radians(rRange[1])+rDelta, rDelta)
    weekBars = [(i*rDelta, rDelta) for i in range(len(deltas)-1)]
    clrsBlocks = [clr(norm(value)) for value in rowMagnitudes]
    ax.broken_barh(
        weekBars, (offset+wpix*height, height), lw=1,
        facecolors=clrsBlocks, edgecolors='#ffffff55'
    )
    ax.text(
        0, offset+wpix*height+height/2, wpnLabel,
        va='center', ha='left', fontsize=fontSize
    )
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_thetamin(0)
ax.set_thetamax(rRange[1])
ax.set_ylim(0, offset+wpnsNumber*height)
ax.set_theta_zero_location(origin)
ax.set_theta_direction(direction)
ax.spines['polar'].set_visible(False)
ax.axis("off")
ax.set_rlabel_position(0)
ax.xaxis.grid(False)
ax.yaxis.grid(False)
plt.savefig(
    path.expanduser('~/Desktop/weaponRank.png'),
    dpi=300, orientation='portrait', format=None,
    facecolor='w', edgecolor='w',
    transparent=True,
    bbox_inches='tight', pad_inches=0, metadata=None
)
