#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import markers
from collections import Counter
from itertools import combinations, product

if splat.isNotebook():
    (iPath, oPath) = (
        path.expanduser('~/Documents/GitHub/s3s_source/'),
        path.expanduser('~/Documents/Sync/BattlesData/')
    )
else:
    (iPath, oPath) = argv[1:]
###############################################################################
# Create Player Objects
###############################################################################
# historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee', 'DantoNnoob'
)
plyr = splat.Player(NAMES[0], bPaths, timezone='America/Los_Angeles')
# (chip, yami, april, richie, memo, tomas) = [
#     splat.Player(nme, bPaths, timezone='America/Los_Angeles')
#     for nme in NAMES
# ]
# team = (chip, yami, april, richie, memo, tomas)
###############################################################################
# Pulling out some stats
###############################################################################
(bHist, bRcrd) = (plyr.battlesHistory, plyr.battleRecords)

# Filter Player History
filters = [
    bHist['winBool']==1,
    bHist['main weapon']=='Splattershot',
    bHist['match type']!='Turf War'
]
fullFilter = [all(i) for i in zip(*filters)]
ix = list(bHist[fullFilter].index)
# Get matching battle records
bRecs = [bRcrd[i] for i in ix]


attsList = []
for bRec in bRecs:
    record = pd.concat(bRec.enemyTeams)
    attribute = set(record['main weapon'])
    attsList.extend(attribute)
freqs = Counter(attsList).most_common()
fracs = [(n, i/len(bRecs)) for (n, i) in freqs]




wpsList = set()
for bRec in bRecs:
    record = pd.concat(bRec.enemyTeams)
    wpsList.update(list(record['main weapon']))

wpCombos = list(product(wpsList, repeat=4))

wpSets = set()
for combo in wpCombos:
    cmb = tuple(Counter(combo).most_common())
    if cmb not in wpSets:
        wpSets.add(cmb)


