#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from os import path
from sys import argv
import SplatStats as splat
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

if splat.isNotebook():
    (plyrName, weapon, mode, overwrite) = ('čħîþ ウナギ', 'All', 'All', 'True')
    (iPath, bPath, oPath) = (
        path.expanduser('~/Documents/Sync/BattlesDocker/jsons'),
        path.expanduser('~/Documents/Sync/BattlesDocker/battles'),
        path.expanduser('~/Documents/Sync/BattlesDocker/out')
    )
    fontPath = '/home/chipdelmal/Documents/GitHub/SplatStats/other/'
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
title = '(Kills+0.5*Assists)/Deaths'
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
# Battle mode filter ----------------------------------------------------------
###############################################################################
# Iris
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
(fig, ax) = splat.plotkillDeathIris(
    (fig, ax), pHist,
    alpha=.9,
    innerGuides=(0, 10, 1), outerGuides=(10, 50, 10),
    fontColor='#000000CC', frameColor="#000000AA",
    innerGuidesColor="#000000BB", outerGuidesColor="#000000BB",
    innerTextFmt='{:.2f}'
)
ax.set_title(title+'\n', fontsize=18)
ax.set_facecolor("w")
ax.set_yticklabels(
    ["", 10, 20, 30, 40], 
    fontdict={'fontsize': 8.5, 'color': '#000000BB', 'ha': 'center'}
)
ax.set_rlabel_position(0)
fig.savefig(
    path.join(oPath, f'{fNameID}_Iris.png'), 
    dpi=300, bbox_inches='tight',
    facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
#  Circle Barchart Kills
###############################################################################
killsTotal = playerHistory['kassist'].sum()
wColors = [
    '#2DD9B6', '#4F55ED', '#B14A8D', '#C70864', '#2CB721', 
    '#4B25C9', '#830B9C', '#C6D314', '#0D37C3', '#C920B7', 
    '#571DB1', '#14BBE7', '#38377A', '#990F2B', '#7F7F99',
][::-1]
(fig, ax) = splat.plotCircularBarchartStat(
    playerHistory, cat='main weapon', stat='kassist', aggFun=np.sum,
    colors=wColors, # yRange=(0, 10e3), 
    logScale=True, ticksStep=10,
    ticksFmt={
        'lw': 1, 'range': (-0.5, -0.25), 
        'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.0f}'
    }
)
ax.set_title(f'(Kills+0.5*Assists) = {killsTotal}\n', fontsize=18)
fig.savefig(
    path.join(oPath, f'{fNameID}_Polar-Kill.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
#  Circle Barchart Wins
###############################################################################
winsTotal = playerHistory['winBool'].sum()
(fig, ax) = splat.plotCircularBarchartStat(
    playerHistory, cat='main weapon', stat='winBool', aggFun=np.sum,
    colors=wColors, # yRange=(0, 10e3), 
    logScale=True, ticksStep=10,
    ticksFmt={
        'lw': 1, 'range': (-0.5, -0.25), 
        'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.0f}'
    }
)
ax.set_title(f'Wins = {winsTotal}\n', fontsize=18)
fig.savefig(
    path.join(oPath, f'{fNameID}_Polar-Win.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Win Ratio
###############################################################################
winsTotal = playerHistory['winBool'].sum()
matchesTotal = playerHistory.shape[0]
winRatio = winsTotal/matchesTotal*100
(metric, aggMetrics) = ('win ratio', ('win', 'total matches'))
df = splat.calcStagesStatsByType(pHist)
dfFlat = splat.ammendStagesStatsByType(df, matchModes=list(df.keys()))
dfFlat.sort_values('match type', inplace=True)
g = splat.plotMatchTypeBars(
    dfFlat, metric, aggMetrics, digs=4,
    yRange=(0, 1), countsLegend={'color': '#00000077', 'fontsize': 7},
    textOffset=0.005, alpha=.98
)
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle(f'Wins = {winRatio:.0f}% ({winsTotal}/{matchesTotal})\n', fontsize=18)
g.savefig(
    path.join(oPath, f'{fNameID}_Bars-Win.png'), 
    dpi=300, bbox_inches='tight'
)
plt.close(g.fig)
###############################################################################
# Kill Ratio
###############################################################################
kassistTotal = np.sum(playerHistory['kassist'])/np.sum(playerHistory['death'])
(metric, aggMetrics) = ('kassists ratio', ('kassists', 'deaths'))
g = splat.plotMatchTypeBars(
    dfFlat, metric, aggMetrics, yRange=(0, 4), digs=4,
    countsLegend={'color': '#00000077', 'fontsize': 7},
    percentage=False, textOffset=0.005, alpha=0.98
)
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle(f'{title} = {kassistTotal:.4f}\n', fontsize=18)
g.savefig(
    path.join(oPath, f'{fNameID}_Bars-Kill.png'), 
    dpi=300, bbox_inches='tight'
)
plt.close(g.fig)
###############################################################################
# Waffle
###############################################################################
(fig, ax) = plt.subplots(figsize=(8, 8))
(fig, ax) = splat.plotWaffleStat(
    (fig, ax), playerHistory,
    function=sum, grouping='main weapon', stat='kassist',
    rows=50, columns=50, vertical=False,
    colors=splat.CLR_CLS_LONG
)
ax.set_title(f'(Kills+0.5*Assists) = {killsTotal}\n', fontsize=18)
fig.savefig(
    path.join(oPath, f'{fNameID}_Waffle-Kill.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Histogram
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 3))
(fig, ax) = splat.plotKillsAndDeathsHistogram(
    (fig, ax), playerHistory, (0, 35), 
    yRange=(-.5, .5), edgecolor='k',
    alpha=0.85,
    normalized=True
)
ax.relim()
ax.autoscale()
(ymin, ymax) = ax.get_ylim()
mxLim = max([abs(ymin), ymax])
ax.set_ylim(-mxLim, mxLim)
ax.set_xlim(0, 40)
ax.set_aspect(.25/ax.get_data_ratio())
plt.savefig(
    path.join(oPath, f'{fNameID}_Histogram-Kill.png'),  
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Awards
###############################################################################
try:
    awds = plyr.getAwardFrequencies()
    (fig, ax) = splat.polarBarChart(
        [i[0] for i in awds[::-1]], 
        [i[1] for i in awds[::-1]],
        labelFmt={
            'color': '#000000EE', 'fontsize': 7.5, 
            'ha': 'left', 'fmt': '{:.1f}'
        },
        colors=[
            '#C70864', '#571DB1', '#C920B7', '#4F55ED', '#B14A8D', '#7F7F99', 
            '#C70864', 
            '#2CB721', '#4B25C9', '#830B9C', '#C6D314', '#0D37C3', 
            '#14BBE7', '#38377A', '#C70864'
        ][::-1]*10
    )
    ax.set_title(f'Awards\n', fontsize=18)
    fig.savefig(
        path.join(oPath, f'{fNameID}_Awards.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
except:
    pass
###############################################################################
# Battle History
###############################################################################
phLen = playerHistory.shape[0]
if phLen > LEN_LIMIT:
    ilocRange = (-LEN_LIMIT, phLen)
else:
    ilocRange = (0, -1)
yRange = ((0, 40), (0, 2000))
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
    yRange=yRange, sizeMultiplier=.8, ilocRange=ilocRange
)
(_, ax_bottom) = splat.plotMatchTypeHistory(
    (fig, ax_bottom), playerHistory, 
    sizeMultiplier=.5, labelsize=4, ilocRange=ilocRange
)
ax_top.tick_params(labelbottom=False)
ax_bottom.set_yticks([])
plt.setp(ax_bottom.get_xticklabels(), rotation=90, ha='right')
plt.savefig(
    path.join(oPath, f'{fNameID}_History.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Ranks
###############################################################################
cats = ['kill', 'death', 'assist', 'paint']
ranksNum = 4
dfRank = plyr.getPlayerAlliedRanking(cats=cats)
(fig, ax) = splat.polarBarRanks(dfRank, ranksNum)
for x in ax:
    x.set_ylim(-ranksNum/ranksNum, ranksNum)
fig.suptitle(f'Team Ranking Frequency\n', fontsize=18)
fig.savefig(
    path.join(oPath, f'{fNameID}_RanksAllied.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
# Full Rank ---------------------------------------------------------------
ranksNum = 8
dfRank = plyr.getPlayerFullRanking(cats=cats)
(fig, ax) = splat.polarBarRanks(
    dfRank, ranksNum, yRange=(0, .5), ticksStep=5
)
for x in ax:
    x.set_ylim(-ranksNum/ranksNum, ranksNum)
fig.suptitle(f'Overall Ranking Frequency\n', fontsize=18)
fig.savefig(
    path.join(oPath, f'{fNameID}_RanksFull.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Player History to Disk
###############################################################################
playerHistory.to_csv(path.join(oPath, f'{plyrName}.csv'))
