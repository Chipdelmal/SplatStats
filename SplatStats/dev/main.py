#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SplatStats as splat
import matplotlib.pyplot as plt

(iPath, oPath) = (
    '/home/chipdelmal/Documents/GitHub/s3s/',
    '/home/chipdelmal/Documents/GitHub/SplatStats/BattlesData'
)
###############################################################################
# Get filepaths
#   Demo names:
#       čħîþ ウナギ, Yami ウナギ, April ウナギ, Riché ウナギ, Oswal　ウナギ, Murazee
###############################################################################
# Create history object
history = splat.History(iPath, oPath)
playerHistory = history.getPlayerHistory('čħîþ ウナギ')
validMatches = playerHistory[playerHistory['win']!='NA']
validMatches

###############################################################################
# Plot K/D ratio
###############################################################################
timeScale = False
(kill, death, matchType, weapon) = (
    list(validMatches['kill']), 
    list(validMatches['death']),
    list(validMatches['match type']),
    list(validMatches['main weapon'])
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
    xPos = hoursDiff[i] if timeScale else i
    # Plot kill to death range ------------------------------------------------
    ax.plot(xPos, kill[i], shape, color=color, alpha=0.3)
    ax.plot(xPos, death[i], shape, color=color, alpha=0.3)
    ax.vlines(xPos, kill[i], death[i], color=color, alpha=0.2)
    # Plot vspan for match type -----------------------------------------------
    ax.axvspan(xPos-.5, xPos+.5, color=colorMT, alpha=.05, lw=0, zorder=-10)
# ax.hlines([0], 0, 1, color='k', transform=ax.get_yaxis_transform())
xLim = max(hoursDiff) if timeScale else mNum
ax.set_xlim(-1, xLim)
ax.set_ylim(-1, max(kill)+1)
ax.set_aspect(.25/ax.get_data_ratio())
ax.set_xticks(list(range(mNum)))
plt.xticks(rotation=90)
ax.set_xticklabels(weapon)