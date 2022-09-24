#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path
import numpy as np
import pandas as pd
import seaborn as sns
import SplatStats as splat
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import markers
from collections import Counter
from matplotlib import pyplot
from math import ceil, floor
import numpy as np
from numpy import linspace
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


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
historyFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(historyFilepaths, oPath)
bPaths = splat.getBattleFilepaths(oPath)
###############################################################################
# Create Player Objects
###############################################################################
NAMES = (
    'čħîþ ウナギ', 'Yami ウナギ', 'Riché ウナギ',
    'Oswal　ウナギ', 'April ウナギ', 'Murazee'
)
plyr = splat.Player(NAMES[3], bPaths, timezone='America/Los_Angeles')
# (chip, yami, april, richie, memo, tomas) = [
#     splat.Player(nme, bPaths, timezone='America/Los_Angeles')
#     for nme in NAMES
# ]
# team = (chip, yami, april, richie, memo, tomas)
playerHistory = plyr.battlesHistory
###############################################################################
# Violin plot
###############################################################################
srs = {
    cat: list(playerHistory[cat]) for cat in ('kill', 'death', 'assist', 'special')
}
srsDF = pd.DataFrame(srs)

# plt.figure(figsize=(10,10))
# # sns.violinplot(data=srsDF)
# # sns.stripplot(data=srsDF, color="k", alpha=0.8, size=2)
# sns.swarmplot(data=srsDF, color="k", alpha=0.8, size=.9)


# pyplot.hist(srsDF['kill'],  50, alpha=0.5, label='kill')
# pyplot.hist(srsDF['death'], 50, alpha=0.5, label='death')
# pyplot.hist(srsDF['assist'], 50, alpha=0.5, label='assist')
# pyplot.hist(srsDF['special'], 50, alpha=0.5, label='special')
###############################################################################
# Histogram
###############################################################################
# dataframe
df = pd.DataFrame({
    'var1': np.array(srsDF['kill'])+np.array(srsDF['assist']*.5), 
    'var2': srsDF['death']
})

# Fig size
(fig, ax) = plt.subplots(figsize=(15, 8))
# plot histogram chart for var1
sns.histplot(x=df.var1, stat="frequency", bins=ceil(max(df['var1'])), edgecolor='black')
n_bins = 10
# get positions and heights of bars
heights, bins = np.histogram(df.var2, density=False, bins=max(df['var2'])) 
# multiply by -1 to reverse it
heights *= -1
bin_width = np.diff(bins)[0]
bin_pos =( bins[:-1] + bin_width / 2) 
# plot
plt.bar(bin_pos, heights, width=bin_width, edgecolor='black')

ax.set_ylim(-25, 25)

# show the graph
plt.show()