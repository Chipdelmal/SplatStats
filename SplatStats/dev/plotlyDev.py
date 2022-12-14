#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import math
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import SplatStats as splat

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

df = splat.calcStagesStatsByType(playerHistory)
dfFlat = splat.ammendStagesStatsByType(df, matchModes=list(df.keys()))
dfFlat = dfFlat[dfFlat['match type']!='Tricolor Turf War']
dfFlat.sort_values('match type', inplace=True)
# Inputs ----------------------------------------------------------------------
stagesByTypeFlat = dfFlat
sorting=[
    'Turf War', 'Tower Control', 'Rainmaker', 
    'Splat Zones', 'Clam Blitz'
]
metric = 'kassists ratio'
aggMetrics = ('kassists', 'deaths')
alpha = 0.9
yRange=(0, 5)
cDict=splat.CLR_STAGE
alpha=0.75
wspace=0.05
hspace=0
aspect=1
fontsize=8
percentLegend={'color': '#00000020', 'fontsize': 50}
countsLegend={'color': '#00000044', 'fontsize': 8}
digs=3
percentage=False
fmt='{:.2f}'
# Plot ------------------------------------------------------------------------
allStages = sorted(stagesByTypeFlat['stage'].unique())
# sns.set(rc={'figure.figsize':(15, 15)})
# Plot --------------------------------------------------------------------
g = sns.FacetGrid(
    stagesByTypeFlat, col="match type", aspect=.75,
    col_order=sorting
)
g.map(
    sns.barplot, 'stage', metric, 
    palette=[cDict[k] for k in allStages], 
    alpha=alpha, order=allStages
)
g.figure.subplots_adjust(wspace=wspace, hspace=hspace)
# g.set_xticklabels(allStages, rotation=90)
g.set_axis_labels('', metric)
g.set_titles('{col_name}')
# Modify axes -------------------------------------------------------------
for ax in g.axes.flatten():
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1)
    ax.set_box_aspect(aspect)
    ax.set_ylim(*yRange)
    ax.set_xticklabels(allStages, fontdict={'fontsize': fontsize})
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_yticklabels(
        [f'{i:.1f}' for i in ax.get_yticks()], 
        fontdict={'fontsize': fontsize}
    )
    mType = ax.get_title()
    fltr = (stagesByTypeFlat['match type'] == mType)
    dataMatchType = stagesByTypeFlat[fltr]
    tmatch = sum(dataMatchType[aggMetrics[1]])
    if (tmatch > 0):
        ratio = sum(dataMatchType[aggMetrics[0]])/tmatch
    else:
        ratio = 0
    if percentage:
        ax.text(
            0.525, 0.5, 
            '{}%'.format(round(ratio*100)), 
            ha='center', va='center',
            transform=ax.transAxes,
            **percentLegend
        )
    else:
        ax.text(
            0.525, 0.5, 
            fmt.format(ratio), 
            ha='center', va='center',
            transform=ax.transAxes,
            **percentLegend
        )
    # Matches counts -------------------------------------------------------
    x_min, x_max = ax.get_xlim()
    ticks = [(tick - x_min)/(x_max - x_min) for tick in ax.get_xticks()]
    for (ix, st) in enumerate(allStages):
        fltrStage = (dataMatchType['stage'] == st)
        stageData = dataMatchType[fltrStage]
        ax.text(
            ticks[ix], .03, 
            '{}'.format(
                str(int(stageData[aggMetrics[1]])).zfill(digs)
            ), 
            ha='center', va='bottom',
            rotation=90,
            transform=ax.transAxes,
            **countsLegend
        )
    ax.text(
        0.975, 0.975, 
        '{}'.format(
            str(sum(dataMatchType[aggMetrics[1]])).zfill(digs)
        ), 
        ha='right', va='top', transform=ax.transAxes,
        **countsLegend
    )
###############################################################################
# Helper Columns
###############################################################################
playerHistory['kpm'] = playerHistory['kill']/playerHistory['duration']
playerHistory['win num'] = [1 if i == 'W' else 0 for i in playerHistory['win']]
###############################################################################
# Treemap
###############################################################################
fig = px.treemap(
    playerHistory, 
    path=['stage', 'match type'], 
    values='win num'
)
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.write_html(path.join(oPath, 'Treemap.html'))
###############################################################################
# BarChart
###############################################################################
sorting=[
    'Turf War', 'Tower Control', 'Rainmaker', 
    'Splat Zones', 'Clam Blitz'
]
yRange=(0, 1)
cDict=splat.CLR_STAGE 
alpha=0.75
wspace=0.05
hspace=0 
aspect=1 
fontsize=8
sorting=[
    'Turf War', 'Tower Control', 'Rainmaker', 
    'Splat Zones', 'Clam Blitz'
]
metric = 'win ratio'

df = splat.calcStagesStatsByType(playerHistory)
dfFlat = splat.ammendStagesStatsByType(df, matchModes=list(df.keys()))
dfFlat = dfFlat[dfFlat['match type']!='Tricolor Turf War']
dfFlat.sort_values('match type', inplace=True)
allStages = sorted(dfFlat['stage'].unique())
# sns.set(rc={'figure.figsize':(15, 15)})
# Plot --------------------------------------------------------------------
g = sns.FacetGrid(
    dfFlat, col="match type", aspect=.75,
    col_order=sorting
)
g.map(
    sns.barplot, 'stage', metric, 
    palette=[cDict[k] for k in allStages], 
    alpha=alpha, order=allStages
)
g.figure.subplots_adjust(wspace=wspace, hspace=hspace)
# g.set_xticklabels(allStages, rotation=90)
g.set_axis_labels('', metric)
g.set_titles('{col_name}')
# Modify axes -------------------------------------------------------------
for ax in g.axes.flatten():
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1)
    ax.set_box_aspect(aspect)
    ax.set_ylim(*yRange)
    ax.set_xticklabels(allStages, fontdict={'fontsize': fontsize})
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_yticklabels(
        [f'{i:.1f}' for i in ax.get_yticks()], 
        fontdict={'fontsize': fontsize}
    )
    mType = ax.get_title()
    fltr = (dfFlat['match type'] == mType)
    tmatch = sum(dfFlat[fltr]['total matches'])
    if (tmatch > 0):
        ratio = sum(dfFlat[fltr]['win'])/tmatch
    ax.text(
        0.525, 0.5, 
        '{}%'.format(round(ratio*100)), 
        ha='center', va='center',
        transform=ax.transAxes,
        color='#00000020', fontsize=50
    )