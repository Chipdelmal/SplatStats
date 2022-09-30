#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import SplatStats as splat

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
