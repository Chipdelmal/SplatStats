
import math
import numpy as np
from os import path
from sys import argv
from matplotlib.patches import Rectangle
import SplatStats as splat
from scipy import interpolate
from os import path
import matplotlib.colors as mcolors
from collections import Counter
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

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
pHist['kassist'] = (pHist['kill']+0.5*pHist['assist'])/pHist['death']
pHist.replace([np.inf, -np.inf], 0, inplace=True)
pHist['participation'] = [1]*pHist.shape[0]
###############################################################################
# Bumpchart
###############################################################################
wpnHist = pHist[['main weapon', 'datetime']]
wpnSet = set(pHist['main weapon'].unique())
# Weapon stats DF ------------------------------------------------------------
wpnGrpBy = pHist.groupby('main weapon').sum('kill').reset_index()
# Weapons frequencies --------------------------------------------------------
weapons = sorted(list(wpnSet))
weaponsCount = pHist.groupby('main weapon').size().sort_values(ascending=False)
# Dates slicer ---------------------------------------------------------------
dteSlice = pHist['datetime'].apply(
    lambda x: "{}/{:02d}".format(x.year, x.week)
).copy()
pHist.insert(3, 'DateGroup', dteSlice)
# Dated Counts ---------------------------------------------------------------
STAT = 'kassist'
RANKS = len(weapons)
HIGHLIGHT = wpnSet
(WIN_W, WIN_M) = (4, 1)
grpd = pHist.groupby(['main weapon', 'DateGroup']).sum('kill')
dfTable = grpd.unstack().reset_index().set_index("main weapon")[STAT]
dfCounts = dfTable.replace(np.nan,0)
# Rank counts ----------------------------------------------------------------
dfRanks = dfCounts.rank(ascending=False, method='dense', axis=0)
dfCountsR = dfCounts.rolling(window=WIN_W, min_periods=WIN_M, axis=1).mean()
dfRanksR = dfCountsR.rank(ascending=False, method='first', axis=0)
cmap = splat.colorPaletteFromHexList([
    '#bde0fe', '#ff0054', '#0a369d', '#33a1fd', '#5465ff', 
    '#f0a6ca', '#ff499e', '#b79ced', '#aaf683', '#f1c0e8'
])


dates = sorted(list(dfCounts.columns))
artists = sorted(list(dfCounts.index))
(aspect, fontSize, lw) = (.2, 5, 1.75)
(hiCol, loCol) = (.85, .15)
(ySpace, colors) = (1, cmap(np.linspace(0, 1, len(artists))))
# random.shuffle(colors)
xExtend = 4
# Stats -----------------------------------------------------------------------
artistsT0 = list(dfRanksR.index)
ranksDate = list(dfRanksR.columns)[WIN_M]
ranksT0 = list(dfRanksR[ranksDate])
ranksDateF = list(dfRanksR.columns)[-1]
ranksTF = list(dfRanksR[ranksDateF])
# Ranks Plot ------------------------------------------------------------------
t = list(range(0, len(dates)+xExtend, 1))
xnew = np.linspace(0, max(t), 500)
yearTicks = [i for i, s in enumerate(dates) if '/01' in s]
years = np.arange(yearTicks[0], yearTicks[-1]+12, 12)
dteTicks = [item[:4] for item in dates if '/01' in item]
(fig, ax) = plt.subplots(1, 1, figsize=(15, 3.5))
for i in range(len(artists)):
    y = RANKS-(np.asarray(dfRanksR.iloc[i])-1)*ySpace
    y[np.isnan(y)]=y[WIN_M]
    z = np.append(y, [y[-1]]*xExtend)
    colors[i][-1] = loCol
    if artists[i] in HIGHLIGHT:
        colors[i][-1] = hiCol
    x = np.arange(y.shape[0])
    xs = np.linspace(0, x[-1], num=1024)
    plt.plot(
        xs, interpolate.pchip(x, y)(xs), 
        lw=lw, color=colors[i]
    )
# ax.vlines(
#     years, 0, 1, 
#     lw=.5, ls=':', transform=ax.get_xaxis_transform(), color='w'
# )
# ax.vlines(
#     [i-6 for i in years[1:]], 0, 1, 
#     lw=.25, ls=':', transform=ax.get_xaxis_transform(), color='w'
# )
for (art, pos) in zip(artistsT0, ranksT0):
    ax.text(
        -1, RANKS-ySpace*(int(pos)-1)-ySpace*.2, art, 
        ha='right', color='k', fontsize=fontSize
    )
for (art, pos) in zip(artistsT0, ranksTF):
    ax.text(
        len(dates)-WIN_W+xExtend, RANKS-ySpace*(int(pos)-1)-ySpace*.2, art, 
        ha='left', color='k', fontsize=fontSize
    )
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_facecolor('w')
ax.get_xaxis().set_ticks(years)
a = ax.get_xticks().tolist()
years = np.arange(int(dteTicks[0]), int(dteTicks[-1])+1, 1)
for i in range(len(a)):
    a[i] = years[i]
# ax.text(t[-1]/2, -1, STAT, va='center')
ax.get_xaxis().set_ticklabels(a)
ax.get_yaxis().set_ticks([])
ax.spines['bottom'].set_color('white')
ax.tick_params(axis='x', colors='white')
ax.set_xlim(ax.get_xlim()[0], len(dates)-1+xExtend)
ax.set_ylim(0, ax.get_ylim()[1])
ax.set_aspect(aspect/ax.get_data_ratio(), adjustable='box')
plt.savefig(
    path.expanduser('~/Desktop/weaponRank.png'),
    dpi=300, orientation='portrait', format=None,
    facecolor='w', edgecolor='w',
    transparent=True,
    bbox_inches='tight', pad_inches=0, metadata=None
)