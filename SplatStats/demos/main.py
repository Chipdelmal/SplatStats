#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import numpy as np
import SplatStats as splat
import matplotlib.pyplot as plt

plyrName = 'čħîþ ウナギ'
(iPath, oPath) = ('./dataJSON', './dataBattle')
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, oPath)
bFilepaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
playerHistory.columns
###############################################################################
# Example of Inspecting and Filtering Dataframe
###############################################################################
filters = (
    playerHistory['main weapon'] == 'Hero Shot Replica',
    playerHistory['stage'] == 'Mincemeat Metalworks',
    playerHistory['kill'] >= 10,
    playerHistory['death'] <= 10,
)
fullFilter = [all(i) for i in zip(*filters)]
playerHistory[fullFilter]
###############################################################################
# Treemap by Match Type
###############################################################################
(matchType, metric) = ("Turf War", "kill ratio")
stagesStatsMatch = splat.calcStagesStatsByType(playerHistory)
stagesDF = stagesStatsMatch[matchType]
(fig, ax) = plt.subplots(figsize=(5, 5))
(fig, ax) = splat.plotTreemapByStages(
    (fig, ax), stagesDF, metric=metric, 
    fmt='{:.2f}', pad=0.1, alpha=.5
)
fig.savefig(
    path.join(oPath, f'Treemap.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Kills (top) vs Deaths (bottom) Histogram
###############################################################################
(fig, ax) = plt.subplots(figsize=(30, 15))
(fig, ax) = splat.plotKillsAndDeathsHistogram(
    (fig, ax), playerHistory, (0, 40), 
    yRange=(-.5, .5), edgecolor='k', normalized=True
)
fig.savefig(
    path.join(oPath, f'Histogram.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Battle History Panel
###############################################################################
yRange = ((0, 40), (0, 1600))
fig = plt.figure(figsize=(30, 5))
gs = fig.add_gridspec(
    2, 1,  
    width_ratios=(1, ), height_ratios=(.75, .05),
    left=0.1, right=0.9, bottom=0.1, top=0.9,
    wspace=0.05, hspace=0
)
ax_top    = fig.add_subplot(gs[0])
ax_bottom = fig.add_subplot(gs[1], sharex=ax_top)
(_, ax_top) = splat.plotMatchHistory(
    (fig, ax_top), playerHistory, 
    yRange=yRange, sizeMultiplier=.8
)
(_, ax_bottom) = splat.plotMatchTypeHistory(
    (fig, ax_bottom), playerHistory, 
    sizeMultiplier=.7, labelsize=4
)
ax_top.tick_params(labelbottom=False)
ax_bottom.set_yticks([])
plt.setp(ax_bottom.get_xticklabels(), rotation=90, ha='right')
fig.savefig(
    path.join(oPath, f'History.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Iris Plot
###############################################################################
(fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
(fig, ax) = splat.plotkillDeathIris(
    (fig, ax), playerHistory,
    innerGuides=(0, 6, 1), outerGuides=(10, 50, 10)
)
###############################################################################
# Wins Barchart
###############################################################################
(metric, aggMetrics) = ('win ratio', ('win', 'total matches'))
df = splat.calcStagesStatsByType(playerHistory)
dfFlat = splat.ammendStagesStatsByType(df, matchModes=list(df.keys()))
# dfFlat = dfFlat[dfFlat['match type']!='Tricolor Turf War']
dfFlat.sort_values('match type', inplace=True)
g = splat.plotMatchTypeBars(dfFlat, metric, aggMetrics, yRange=(0, 1))
g.savefig(
    path.join(oPath, f'Barcharts.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Ranks
###############################################################################
cats = ['kill', 'death', 'assist', 'special', 'paint']
dfRank = plyr.getPlayerAlliedRanking(cats=cats)
(fig, axes) = plt.subplots(figsize=(10, 10), nrows=len(cats), sharex=True)
(fig, axes) = splat.plotRanking(
    (fig, axes), dfRank, 
    normalized=True, xLim=(-.6, 3.6), yLim=(0, 0.75)
)
fig.savefig(
    path.join(oPath, f'RanksAllied.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
# Full Rank -------------------------------------------------------------------
dfRank = plyr.getPlayerFullRanking(cats=cats)
(fig, axes) = plt.subplots(
    figsize=(10, 10), nrows=len(cats), sharex=True
)
(fig, axes) = splat.plotRanking(
    (fig, axes), dfRank, 
    normalized=True, xLim=(-.6, 7.6), yLim=(0, 0.5)
)
fig.savefig(
    path.join(oPath, f'Ranks.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
#  Waffle
###############################################################################
(fig, ax) = plt.subplots(figsize=(8, 8))
(fig, ax) = splat.plotWaffleStat(
    (fig, ax), playerHistory,
    function=sum, grouping='main weapon', stat='kill',
    colors=splat.CLR_CLS_LONG
)
fig.savefig(
    path.join(oPath, f'Waffle.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
#  Circle Barchart
###############################################################################
wColors = [
    '#2DD9B6', '#4F55ED', '#B14A8D', '#7F7F99', '#990F2B',
    '#C70864', '#2CB721', '#4B25C9', '#830B9C', '#C6D314',
    '#0D37C3', '#C920B7', '#571DB1', '#14BBE7', '#38377A'
][::-1]
(fig, ax) = splat.plotCircularBarchartStat(
    playerHistory, cat='main weapon', stat='kassist', aggFun=np.sum,
    colors=wColors, yRange=(0, 10e3), logScale=True, ticksStep=10,
    ticksFmt={
        'lw': 1, 'range': (-0.5, -0.25), 
        'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.0f}'
    }
)
fig.savefig(
    path.join(oPath, f'Polar.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)