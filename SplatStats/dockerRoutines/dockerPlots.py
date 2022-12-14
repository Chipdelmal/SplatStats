#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from os import path
from sys import argv
import SplatStats as splat
import matplotlib.pyplot as plt

if splat.isNotebook():
    (plyrName, weapon, mode) = ('čħîþ ウナギ', 'Splattershot', 'All')
    (iPath, bPath, oPath) = (
        path.expanduser('~/Documents/WorkSims/SplatStats/jsons'),
        path.expanduser('~/Documents/WorkSims/SplatStats/battles'),
        path.expanduser('~/Documents/WorkSims/SplatStats/out')
    )
    fontPath = './SplatStats/'
else:
    (plyrName, weapon, mode) = argv[1:]
    (iPath, bPath, oPath) = ('/data/jsons', '/data/battles', '/data/out')
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
wColors = [
    '#2DD9B6', '#4F55ED', '#B14A8D', '#7F7F99', '#C70864', 
    '#2CB721', '#4B25C9', '#830B9C', '#C6D314', '#0D37C3', 
    '#C920B7', '#571DB1', '#14BBE7', '#38377A', '#990F2B'
][::-1]
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
(metric, aggMetrics) = ('win ratio', ('win', 'total matches'))
df = splat.calcStagesStatsByType(pHist)
dfFlat = splat.ammendStagesStatsByType(df, matchModes=list(df.keys()))
dfFlat.sort_values('match type', inplace=True)
g = splat.plotMatchTypeBars(
    dfFlat, metric, aggMetrics, 
    yRange=(0, 1), countsLegend={'color': '#00000044', 'fontsize': 8},
    textOffset=0.005, alpha=0.85
)
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle('Wins\n', fontsize=18)
g.savefig(
    path.join(oPath, f'{fNameID}_Bars-Win.png'), 
    dpi=300, bbox_inches='tight'
)
plt.close(g.fig)
###############################################################################
# Kill Ratio
###############################################################################
(metric, aggMetrics) = ('kassists ratio', ('kassists', 'deaths'))
g = splat.plotMatchTypeBars(
    dfFlat, metric, aggMetrics, yRange=(0, 4),
    percentage=False, textOffset=0.005, alpha=0.85
)
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle(title+'\n', fontsize=18)
g.savefig(
    path.join(oPath, f'{fNameID}_Bars-Kill.png'), 
    dpi=300, bbox_inches='tight'
)
plt.close(g.fig)
###############################################################################
# Player History to Disk
###############################################################################
playerHistory.to_csv(path.join(oPath, f'{plyrName}.csv'))