#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
from collections import Counter
import SplatStats as splat
from pywaffle import Waffle
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import Normalize
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
# plt.rcParams["font.family"]="Roboto Mono"


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Create Player Objects
###############################################################################
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'DantoNnoob',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 'Rei ウナギ'
)
plyr = splat.Player(NAMES[0], bPaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
###############################################################################
# Streaks
###############################################################################
wins = list(playerHistory['win'])
splat.longestRun(wins, elem='W')
splat.longestRun(wins, elem='L')
###############################################################################
# Player ranking
###############################################################################
df = plyr.getPlayerFullRanking()

cols = ['#C70864', '#C920B7', '#4B25C9', '#830B9C', '#2CB721']
cats = ['kill', 'death', 'assist', 'special', 'paint']
normalized = False
yLim = None

(fig, axes) = plt.subplots(figsize=(10, 10), nrows=len(cats), sharex=True)
splat.plotRanking((fig, axes), df, normalized=True, yLim=0.5)


for (col, ax, cat) in zip(cols, axes, cats):
    df[cat].value_counts(normalize=normalized).sort_index().plot(
        ax=ax, kind='bar', color=col, width=.9,
        title=cat, xlabel='Rank'
    )
    if yLim:
        ax.set_ylim(0, yLim)



(fig, ax) = plt.subplots()
(fig, ax) = plt.subplots()
df['death'].value_counts().sort_index().plot(ax=ax, kind='bar')





fig = plt.figure(figsize=(30, 5))
gs = fig.add_gridspec(
    2, 1,  
    width_ratios=(1, ), height_ratios=(.75, .05),
    left=0.1, right=0.9, bottom=0.1, top=0.9,
    wspace=0.05, hspace=0
)
ax_top    = fig.add_subplot(gs[0])
ax_bottom = fig.add_subplot(gs[1], sharex=ax_top)




cats = ['kill', 'death', 'assist', 'special', 'paint']
vals = []
for cat in cats:
    dct = Counter(df[cat])
    counts = sorted(dct.items(), key=lambda x: x[0])[::1]
    print(counts)
    vals.append([i[1] for i in counts])

vArray = np.asarray(vals).T
normArray = np.asarray([r/np.sum(r) for r in vArray])


colors = []

x = list(range(1, 6))
for (i, row) in enumerate(vArray):
    plt.bar(x, row)


colors = []
dfS = pd.DataFrame.from_dict({
    i: df[i].value_counts() for i in cats
})
dfS.T.plot.barh(stacked=True, legend=True)


dfS.index.name = 'rank'
dfS.reset_index(inplace=True)

dfS.set_index('rank').plot(kind='bar', stacked=True)


df.plot(x='rank', kind='bar', stacked=True)


dfA = df.drop('datetime', axis=1)
sns.countplot(dfA.melt(value_vars=dfA.columns), y='value', hue='variable')




###############################################################################
# Windowed average
###############################################################################
kSize = 10
dHist = splat.aggregateStatsByPeriod(playerHistory, period='2H')
winsArray = np.asarray((dHist['kassist'])/dHist['matches'])
windowAvg = splat.windowAverage(winsArray, kernelSize=kSize, mode='valid')

(fig, ax) = plt.subplots(figsize=(10, 4))
ax.plot(winsArray, lw=5, color=splat.LUMIGREEN_V_DFUCHSIA_S1[-1], alpha=.15)
ax.plot(
    [i+kSize/2 for i in range(len(windowAvg))], windowAvg,
    lw=4, color=splat.PINK_V_GREEN_S1[0], alpha=.85
)
ax.autoscale(enable=True, axis='x', tight=True)
ax.set_ylim(0, max(winsArray))
###############################################################################
#  Waffle Dev
###############################################################################
alpha = .45
colors = [
    i+splat.alphaToHex(alpha) for i in splat.CLR_CLS_LONG[:len(df['main weapon'])]
]
(fig, ax) = plt.subplots(figsize=(15, 7.5))
ax.set_aspect(aspect="equal")
Waffle.make_waffle(
    ax=ax,
    rows=25, 
    # columns=50,
    values=df['kills'],
    labels=list(df['main weapon']),
    starting_location='NW',
    vertical=False,
    block_arranging_style='snake',
    colors=colors,
    interval_ratio_x=.5,
    interval_ratio_y=.5,
    # labels=[f"{k} ({int(v / sum(data.values()) * 100)}%)" for k, v in data.items()],
    legend={
        'loc': 'lower left',
        'bbox_to_anchor': (0, -.5),
        'ncol': 5,
        'framealpha': 0,
        'fontsize': 12
    }
)
plt.title('kills')
fig.savefig(
    path.join(oPath, (plyr.name)+' Waffle.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)

