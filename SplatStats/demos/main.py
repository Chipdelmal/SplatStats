#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SplatStats as splat
import matplotlib.pyplot as plt

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
plyrName = 'čħîþ ウナギ'
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
playerHistory.columns
###############################################################################
# Inspecting and Filtering Dataframe
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
###############################################################################
# Kills (top) vs Deaths (bottom) Histogram
###############################################################################
(fig, ax) = plt.subplots(figsize=(30, 15))
(fig, ax) = splat.plotKillsAndDeathsHistogram(
    (fig, ax), playerHistory, (0, 40), 
    yRange=(-.5, .5), edgecolor='k', normalized=True
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