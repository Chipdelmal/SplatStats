#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import SplatStats as splat
import matplotlib.pyplot as plt

(iPath, oPath) = (
    '/home/chipdelmal/Documents/GitHub/s3s/',
    '/home/chipdelmal/Documents/GitHub/SplatStats/BattlesData'
)
demoNames = [
    'čħîþ ウナギ', 'Yami ウナギ', 'April ウナギ', 
    'Riché ウナギ', 'Oswal　ウナギ', 'Murazee']
plyrNme = demoNames[0]
###############################################################################
# Get filepaths
###############################################################################
# Create history object
history = splat.History(iPath, oPath)
playerHistory = history.getPlayerHistory(plyrNme)
validMatches = playerHistory[playerHistory['win']!='NA']
validMatches

###############################################################################
# Plot K/D ratio
###############################################################################
timeScale = False
(kill, death, matchType, weapon, win, special) = (
    list(validMatches['kill']), 
    list(validMatches['death']),
    list(validMatches['match type']),
    list(validMatches['main weapon']),
    list(validMatches['win']),
    list(validMatches['special']),
)
dates = list(validMatches['datetime'])
hoursDiff = [(d-min(dates)).seconds/3600  for d in dates]
# Use match type for point shape ----------------------------------------------
mNum = len(matchType)
(fig, ax) = plt.subplots(figsize=(30, 15))
for i in range(mNum):
    # Get shape and color for markers and lines -------------------------------
    shape = 'o' if matchType[i] != 'Turf War' else 'o'
    color = 'blue' if kill[i] >= death[i] else 'red'
    colorMT = 'white' if matchType[i] == 'Turf War' else 'purple'
    colorWL = 'green' if win[i] == 'W' else 'red'
    shapeWL = r'$\uparrow$' if win[i] == 'W' else r'$\downarrow$'
    xPos = hoursDiff[i] if timeScale else i
    # Plot kill to death range ------------------------------------------------
    ax.plot(xPos, kill[i], 'o', color=color, alpha=0.35, zorder=1)
    ax.plot(xPos, death[i], 'X', color=color, alpha=0.35, zorder=1)
    ax.vlines(xPos, kill[i], death[i], color=color, alpha=0.2, zorder=2)
    # Specials and W/L --------------------------------------------------------
    ax.plot(xPos, special[i], "_", color='k', alpha=0.2, zorder=0)
    ax.plot(xPos, -1, marker=shapeWL, color=colorWL, alpha=0.3, zorder=0, markersize=10)
    # Plot vspan for match type -----------------------------------------------
    ax.axvspan(xPos-.5, xPos+.5, color=colorMT, alpha=.05, lw=0, zorder=-10)
    # ax.vlines(
    #     [xPos], 0, 1, color=colorWL, alpha=.1,
    #     transform=ax.get_xaxis_transform(), zorder=-15
    # )
# ax.hlines([0], 0, 1, color='k', transform=ax.get_yaxis_transform())
xLim = max(hoursDiff) if timeScale else mNum
ax.set_xlim(-1, xLim)
ax.set_ylim(-2, max(max(kill), max(death))+1)
ax.set_aspect(.25/ax.get_data_ratio())
ax.set_xticks(list(range(mNum)))
plt.xticks(rotation=90)
ax.set_xticklabels(weapon)
plt.savefig(
    path.join(oPath, plyrNme+'-KDratio.png'), 
    dpi=300, bbox_inches='tight'
)