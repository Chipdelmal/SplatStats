#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
import SplatStats as splat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Rectangle


if splat.isNotebook():
    (iPath, oPath) = (
        '/home/chipdelmal/Documents/GitHub/s3s/',
        '/home/chipdelmal/Documents/GitHub/SplatStats/BattlesData'
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
    'Oswal　ウナギ', 'April ウナギ', 'Murazee'
)
for name in NAMES:
    plyr = splat.Player(name, bPaths, timezone='America/Los_Angeles')
    playerHistory = plyr.battlesHistory
    ###########################################################################
    # Histogram
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(30, 15))
    (fig, ax) = splat.plotKillsAndDeathsHistogram(
        (fig, ax), playerHistory, (0, 40), yRange=(-.25, .25), edgecolor='k',
        normalized=True
    )
    plt.savefig(
        path.join(oPath, (plyr.name)+' KDHistogram.png'), 
        dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
plt.savefig(
    path.join(oPath, (plyr.name)+' BHistory.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)