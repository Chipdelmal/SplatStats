#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from os import path
from sys import argv
import SplatStats as splat
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

if splat.isNotebook():
    (plyrName, weapon, mode) = ('čħîþ ウナギ', 'All', 'All')
    (iPath, bPath, oPath) = (
        path.expanduser('~/Documents/WorkSims/SplatStats/jsons'),
        path.expanduser('~/Documents/WorkSims/SplatStats/battles'),
        path.expanduser('~/Documents/WorkSims/SplatStats/out')
    )
    fontPath = './SplatStats/'
else:
    (plyrName, weapon, mode) = argv[1:]
    (iPath, bPath, oPath) = (
        '/data/jsons', 
        '/data/battles', 
        '/data/out'
    )
    fontPath = '/other/'
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
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=False)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Player Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
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
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
#  Circle Barchart Kills
###############################################################################
killsTotal = playerHistory['kassist'].sum()
wColors = [
    '#2DD9B6', '#4F55ED', '#B14A8D', '#7F7F99', '#C70864', 
    '#2CB721', '#4B25C9', '#830B9C', '#C6D314', '#0D37C3', 
    '#C920B7', '#571DB1', '#14BBE7', '#38377A', '#990F2B'
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
(fig, ax) = plt.subplots(figsize=(12, 3.4))
(fig, ax) = splat.plotWaffleStat(
    (fig, ax), playerHistory,
    function=sum, grouping='main weapon', stat='kassist',
    rows=30, columns=100, vertical=False,
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
    (fig, ax) = plt.subplots(figsize=(10, 4))
    (fig, ax) = splat.plotAwardFrequencies(
        (fig, ax), awds,
        textSize=6, color=wColors,
        alpha=.975
    )
    fig.savefig(
        path.join(oPath, f'Awards - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
except:
    pass
###############################################################################
# Player History to Disk
###############################################################################
playerHistory.to_csv(path.join(oPath, f'{plyrName}.csv'))