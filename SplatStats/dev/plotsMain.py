#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import SplatStats as splat
import matplotlib.pyplot as plt

if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s_source/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
LEN_LIMIT = 400
###############################################################################
# Create Player Objects
##############################################################################
historyFilepaths = splat.getDataFilepaths(iPath)
bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath, overwrite=True)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'DantoNnoob',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 'Rei ウナギ', 'HSR'
)
name = 'čħîþ ウナギ'
for name in NAMES:
    plyr = splat.Player(name, bPaths, timezone='America/Los_Angeles')
    playerHistory = plyr.battlesHistory
    phLen = playerHistory.shape[0]
    if phLen > LEN_LIMIT:
        ilocRange = (-LEN_LIMIT, phLen)
    else:
        ilocRange = (0, -1)
    ###########################################################################
    # Histogram
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(30, 15))
    (fig, ax) = splat.plotKillsAndDeathsHistogram(
        (fig, ax), playerHistory, (0, 40), yRange=(-.25, .25), edgecolor='k',
        normalized=True
    )
    plt.savefig(
        path.join(oPath, f'Histogram - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    # Ranks
    ###########################################################################
    cats = ['kill', 'death', 'assist', 'special', 'paint']
    dfRank = plyr.getPlayerAlliedRanking(cats=cats)
    (fig, axes) = plt.subplots(figsize=(10, 10), nrows=len(cats), sharex=True)
    (fig, axes) = splat.plotRanking(
        (fig, axes), dfRank, 
        normalized=True, xLim=(-.6, 3.6), yLim=(0, 0.75)
    )
    fig.savefig(
        path.join(oPath, f'RankAllied - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    # Full Rank ---------------------------------------------------------------
    dfRank = plyr.getPlayerFullRanking(cats=cats)
    (fig, axes) = plt.subplots(
        figsize=(10, 10), nrows=len(cats), sharex=True
    )
    (fig, axes) = splat.plotRanking(
        (fig, axes), dfRank, 
        normalized=True, xLim=(-.6, 7.6), yLim=(0, 0.5)
    )
    fig.savefig(
        path.join(oPath, f'RankFull - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    # Battle History
    ###########################################################################
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
        path.join(oPath, f'History - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    # Iris
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    (fig, ax) = splat.plotkillDeathIris(
        (fig, ax), playerHistory,
        # colorsTop=('#4F55ED', '#CB0856'),
        # colorBars='#4F55ED',
        innerGuides=(0, 10, 1), 
        outerGuides=(10, 50, 10),
        fontColor='#00000066',
        innerGuidesColor="#00000033",
        outerGuidesColor="#00000011",
        frameColor="#000000AA",
        innerTextFmt='{:.2f}'
    )
    ax.set_facecolor("w")
    ax.set_yticklabels(
        ["", 10, 20, 30, 40], 
        fontdict={'fontsize': 8.5, 'color': '#00000022'}
    )
    ax.set_rlabel_position(0)
    fig.savefig(
        path.join(oPath, f'Iris - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    # Win Ratio
    ###########################################################################
    (metric, aggMetrics) = ('win ratio', ('win', 'total matches'))
    df = splat.calcStagesStatsByType(playerHistory)
    dfFlat = splat.ammendStagesStatsByType(df, matchModes=list(df.keys()))
    # dfFlat = dfFlat[dfFlat['match type']!='Tricolor Turf War']
    dfFlat.sort_values('match type', inplace=True)
    g = splat.plotMatchTypeBars(dfFlat, metric, aggMetrics, yRange=(0, 1))
    g.savefig(
        path.join(oPath, f'MatchesWin - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight'
    )
    plt.close(g.fig)
    ###########################################################################
    # Kill Ratio
    ###########################################################################
    (metric, aggMetrics) = ('kassists ratio', ('kassists', 'deaths'))
    g = splat.plotMatchTypeBars(
        dfFlat, metric, aggMetrics, yRange=(0, 4),
        percentage=False
    )
    g.savefig(
        path.join(oPath, f'MatchesKill - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight'
    )
    plt.close(g.fig)
    ###########################################################################
    #  Waffle
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(8, 8))
    (fig, ax) = splat.plotWaffleStat(
        (fig, ax), playerHistory,
        function=sum, grouping='main weapon', stat='kill',
        rows=50, columns=50,
        colors=splat.CLR_CLS_LONG
    )
    fig.savefig(
        path.join(oPath, f'WaffleKill - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    #  Circle Barchart
    ###########################################################################
    wColors = [
        '#2DD9B6', '#4F55ED', '#B14A8D', '#7F7F99', '#C70864', 
        '#2CB721', '#4B25C9', '#830B9C', '#C6D314', '#0D37C3', 
        '#C920B7', '#571DB1', '#14BBE7', '#38377A', '#990F2B'
    ][::-1]
    (fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    (fig, ax) = splat.plotCircularBarchartStat(
        (fig, ax),
        playerHistory, 'main weapon', 'kassist', np.sum,
        xRange=(0, 7.5e3),
        autoRange=False, colors=wColors
    )
    fig.savefig(
        path.join(oPath, f'PolarKill - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    (fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    (fig, ax) = splat.plotCircularBarchartStat(
        (fig, ax),
        playerHistory, 'main weapon', 'kassist', np.mean,
        xRange=(0, 10), logScale=False,
        autoRange=False, colors=wColors
    )
    fig.savefig(
        path.join(oPath, f'PolarKmean - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    # Win Ratio
    ###########################################################################
    try:
        awds = plyr.getAwardFrequencies()
        (fig, ax) = plt.subplots(figsize=(10, 4))
        (fig, ax) = splat.plotAwardFrequencies((fig, ax), awds)
        fig.savefig(
            path.join(oPath, f'Awards - {plyr.name}.png'), 
            dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
        )
        plt.close()
    except:
        pass
###############################################################################
# Legend
###############################################################################
(fig, ax) = plt.subplots(figsize=(1, 5))
(fig, ax) = splat.generateMatchHistoryLegend((fig, ax))
plt.savefig(
    path.join(oPath, 'Legend.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()

