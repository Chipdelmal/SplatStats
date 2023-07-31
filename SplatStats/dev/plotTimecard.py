
import math
import numpy as np
from os import path
from sys import argv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import LogNorm
import SplatStats as splat
from scipy import interpolate
from os import path
from matplotlib import colors
from math import radians, log10
import matplotlib.colors as mcolors
from collections import Counter
import warnings
warnings.filterwarnings("ignore")


if splat.isNotebook():
    (plyrName, weapon, mode, overwrite) = ('April ウナギ', 'All', 'All', 'False')
    (iPath, bPath, oPath) = (
        path.expanduser('~/Documents/BattlesDocker/jsons'),
        path.expanduser('~/Documents/BattlesDocker/battles'),
        path.expanduser('~/Documents/BattlesDocker/out')
    )
    fontPath = '~/Documents/BattlesDocker/'
else:
    (plyrName, weapon, mode, overwrite) = argv[1:]
    (iPath, bPath, oPath) = (
        '/data/jsons', 
        '/data/battles', 
        '/data/out'
    )
    fontPath = '/other/'
overwrite = (True if overwrite=="True"  else False)
LEN_LIMIT = 400
###############################################################################
# Auxiliary 
###############################################################################
fNameID = f'{plyrName}-{weapon}'
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=overwrite)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Player Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
playerHistory = playerHistory[playerHistory['match mode']!='PRIVATE']
# Weapon filter ---------------------------------------------------------------
if weapon != 'All':
    pHist = playerHistory[playerHistory['main weapon']==weapon]
else:
    pHist = playerHistory
    tCards = splat.getTimecard(playerHistory)
###############################################################################
# Strips
###############################################################################
STAT = 'duration'
tCard = tCards[STAT]
# Auxiliary variables --------------------------------------------------------
wpnSorting = tCard.sum(axis=1).sort_values(ascending=False)
wpnsNumber = len(wpnSorting)
fontSize = np.interp(wpnsNumber, [1, 10, 30, 50], [30, 20, 14, 5])
splat.plotTimecard(
    tCard, wpnSorting, 
    fontSize=fontSize, statScaler=60,
    highColors=['#DE0B64AA', '#311AA8AA', '#6BFF00AA', '#9030FFAA', '#B62EA7AA']
)
