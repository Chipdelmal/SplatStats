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
        path.expanduser('~/Documents/GitHub/s3s/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Load battle paths
###############################################################################
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Team Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ', 'Oswal　ウナギ', 
    'April ウナギ', 'Rei ウナギ', 'DantoNnoob', 'Murazee'
)
TZ = 'America/Los_Angeles'
team = splat.Team(NAMES, bPaths, TZ)
team.reshapeTeamHistoryByPeriod(period='2H')
