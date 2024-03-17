#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sys import argv
from os import path
import SplatStats as splat
from scipy import stats
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
from SplatStats.Player import Player
from SplatStats.constants import MKR_STATS


if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('/Users/chipdelmal/Documents/BattlesDocker/jsons'),
        path.expanduser('/Users/chipdelmal/Documents/BattlesDocker/battles')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################a
# Load battle paths
###############################################################################
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Team Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'April ウナギ', 
    'Rei ウナギ', 'Oswal　ウナギ', 'DantoNnoob', 'Murazee'
)
COLORS = (
    
)
TZ = 'America/Los_Angeles'
team = splat.Team(NAMES, bPaths, TZ)
teamHist = team.battleHistory
teamHistBT = team.reshapeTeamHistoryByPeriod(
    period='2H'
)
###############################################################################
# Plotting Stream
###############################################################################
