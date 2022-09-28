#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
import seaborn as sns
import SplatStats as splat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from SplatStats.plots import plotMatchTypeHistory


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
plyr = splat.Player(NAMES[0], bPaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
###############################################################################
# Plot Dev
###############################################################################
yRange = (0, 50)
fig = plt.figure(figsize=(30, 15))
gs = fig.add_gridspec(
    2, 1,  
    width_ratios=(1, ), height_ratios=(1, .05),
    left=0.1, right=0.9, bottom=0.1, top=0.9,
    wspace=0.05, hspace=0
)
(ax_top, ax_bottom) = (fig.add_subplot(gs[0]), fig.add_subplot(gs[1]))
# Main panel ------------------------------------------------------------------
# autoRange = (0, max(max(kill), max(death)))
# (ymin, ymax) = (yRange if yRange else autoRange)
# Bottom Panel ----------------------------------------------------------------
(_, ax_top) = splat.plotMatchTypeHistory((fig, ax_top), playerHistory)
(_, ax_bottom) = splat.plotMatchTypeHistory((fig, ax_bottom), playerHistory)