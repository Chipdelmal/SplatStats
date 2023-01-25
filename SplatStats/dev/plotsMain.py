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
bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath, overwrite=False)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Setup Splats Font
###############################################################################
splat.setSplatoonFont(oPath, fontName="Splatfont 2")
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'Murazee', 'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'DantoNnoob',
    'Oswal　ウナギ', 'April ウナギ', 'Rei ウナギ', 'HSR'
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
    (fig, ax) = plt.subplots(figsize=(10, 3))
    (fig, ax) = splat.plotKillsAndDeathsHistogram(
        (fig, ax), playerHistory, (0, 35), 
        yRange=(-.25, .25), edgecolor='k',
        alpha=0.85,
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
    cats = ['kill', 'death', 'assist', 'paint']
    dfRank = plyr.getPlayerAlliedRanking(cats=cats)
    (fig, ax) = splat.polarBarRanks(dfRank, 4)
    fig.savefig(
        path.join(oPath, f'RankAllied - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    # Full Rank ---------------------------------------------------------------
    dfRank = plyr.getPlayerFullRanking(cats=cats)
    (fig, ax) = splat.polarBarRanks(dfRank, 8)
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
    (fig, ax) = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
    (fig, ax) = splat.plotkillDeathIris(
        (fig, ax), playerHistory,
        # colorsTop=('#4F55ED', '#CB0856'),
        # colorBars='#4F55ED',
        alpha=.9,
        innerGuides=(0, 10, 1), 
        outerGuides=(10, 50, 10),
        fontColor='#000000CC',
        innerGuidesColor="#000000BB",
        outerGuidesColor="#000000BB",
        frameColor="#000000AA",
        innerTextFmt='{:.2f}'
    )
    ax.set_facecolor("w")
    ax.set_yticklabels(
        ["", 10, 20, 30, 40], 
        fontdict={'fontsize': 8.5, 'color': '#000000BB', 'ha': 'center'}
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
    g = splat.plotMatchTypeBars(
        dfFlat, metric, aggMetrics, 
        yRange=(0, 1), countsLegend={'color': '#00000044', 'fontsize': 8},
        textOffset=0.005, alpha=0.85
    )
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
        percentage=False, textOffset=0.005, alpha=0.85
    )
    g.savefig(
        path.join(oPath, f'MatchesKill - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight'
    )
    plt.close(g.fig)
    ###########################################################################
    # Waffle
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(12, 3.4))
    (fig, ax) = splat.plotWaffleStat(
        (fig, ax), playerHistory,
        function=sum, grouping='main weapon', stat='kassist',
        rows=30, columns=100, vertical=False,
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
    (fig, ax) = splat.plotCircularBarchartStat(
        playerHistory, cat='main weapon', stat='kassist', aggFun=np.sum,
        colors=wColors, yRange=(0, 10e3), logScale=True, ticksStep=10,
        ticksFmt={
            'lw': 1, 'range': (-0.5, -0.25), 
            'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.0f}'
        }
    )
    fig.savefig(
        path.join(oPath, f'PolarKill - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    (fig, ax) = splat.plotCircularBarchartStat(
        playerHistory, cat='main weapon', stat='kassist', aggFun=np.mean,
        colors=wColors, yRange=(0, 10), logScale=False, ticksStep=12,
        ticksFmt={
            'lw': 1, 'range': (-0.5, -0.25), 
            'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.0f}'
        }
    )
    fig.savefig(
        path.join(oPath, f'PolarKmean - {plyr.name}.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
    ###########################################################################
    # Awards
    ###########################################################################
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
