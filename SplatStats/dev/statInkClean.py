# !/usr/bin/env python3

# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

from os import path, system
from glob import glob
import numpy as np
import pandas as pd
from random import shuffle
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
import SplatStats as splat


(six, USR) = (0, 'lab')
SSON = ['Drizzle Season 2022', 'Chill Season 2022', 'Fresh Season 2023']
SEASON = SSON[six]
TOP = 20
###############################################################################
# Get files and set font
###############################################################################
if USR=='lab':
    DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
elif USR=='lap':
    DATA_PATH = '/Users/sanchez.hmsc/Documents/SyncMega/BattlesDocker'
else:
    DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
###############################################################################
# Filter by Constraints
###############################################################################
fltrs = (btls['season']==SEASON, )
fltrBool = [all(i) for i in zip(*fltrs)]
btlsFiltered = btls[fltrBool]
###############################################################################
# Get Total Season Frequencies
###############################################################################
(wpnFreq, wpnWLT, lbyFreq) = (
    splat.getWeaponsFrequencies(btlsFiltered),
    splat.getWeaponsWLT(btlsFiltered),
    splat.getLobbyFrequencies(btlsFiltered)
)
# Checks for consistency ------------------------------------------------------
tests = [
    np.sum(list(wpnFreq.values()))/8 == btlsFiltered.shape[0],
    np.sum(list(lbyFreq.values())) == btlsFiltered.shape[0],
    np.sum(np.sum(wpnWLT[1][:,2])) == np.sum(list(wpnFreq.values()))
]
assert(all(tests))






(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
np.sum(np.sum(matrix, axis=1))/16


ix = names.index('.52 Gal')
np.sum(matrix[:,ix])

cntr = Counter(btlsFiltered['lobby'])

statInkBattles = btlsFiltered
wpnsNames = None

(btls, btlsNum) = (statInkBattles, statInkBattles.shape[0])
# Get weapons used by each team, and who won ------------------------------
tmsWpns = splat.getTeamsWeapons(btls)
(alpha, bravo) = (tmsWpns['alpha'], tmsWpns['bravo'])
winAlpha = list(btls['win'])
# Get all the weapons used, and sort them if needed -----------------------
if not wpnsNames:
    wpnsSet = (set(alpha.stack()) | set(bravo.stack()))
    wpnsNames = sorted(list(wpnsSet))
wpnsNumbr = len(wpnsNames)
# Generate matrix ---------------------------------------------------------
domMtx = np.zeros((wpnsNumbr, wpnsNumbr))
for bix in range(btlsNum):
    # Get names for weapons in both teams ---------------------------------
    (wpnsNmA, wpnsNmB) = (list(alpha.iloc[bix]), list(bravo.iloc[bix]))
    # Get indices for weapons in both teams -------------------------------
    (wpnsIxA, wpnsIxB) = (
        [wpnsNames.index(w) for w in wpnsNmA],
        [wpnsNames.index(w) for w in wpnsNmB]
    )
    if winAlpha[bix]:
        # Team Alpha won --------------------------------------------------
        for ixA in wpnsIxA:
            for ixB in wpnsIxB:
                domMtx[ixA, ixB] = domMtx[ixA, ixB] + 1
    else:
        # Team Bravo won --------------------------------------------------
        for ixB in wpnsIxB:
            for ixA in wpnsIxA:
                domMtx[ixB, ixA] = domMtx[ixB, ixA] + 1