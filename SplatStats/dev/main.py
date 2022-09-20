#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SplatStats as splat

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
validMatches