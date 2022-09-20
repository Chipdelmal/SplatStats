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
# Get the battles filepaths
playerHistory = history.getPlayerHistory('čħîþ ウナギ')
validMatches = playerHistory[playerHistory['win']!='NA']
(k, d) = (list(validMatches['kill']), list(validMatches['death']))
t = list(validMatches['match type'])

# Use match type for point shape
(fig, ax) = plt.subplots(figsize=(20, 8))
for i in range(len(k)):
    shape = 'X' if t[i] != 'Turf War' else 'o'
    color = 'blue' if k[i] >= d[i] else 'red'
    ax.plot(i, k[i], shape, color=color, alpha=0.3)
    ax.plot(i, d[i], shape, color=color, alpha=0.3)
    ax.vlines(i, k[i], d[i], color=color, alpha=0.2)
# ax.hlines([0], 0, 1, color='k', transform=ax.get_yaxis_transform())
ax.set_aspect(.5/ax.get_data_ratio())
ax.set_xlim(-1, len(k))
ax.set_ylim(-1, max(k)+1)

