
# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

import re
import pandas as pd
from os import path
from glob import glob
import matplotlib.pyplot as plt
from collections import Counter
import SplatStats as splat

DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/battle-results-csv'
FPATHS = glob(path.join(DATA_PATH, '*-*-*.csv'))
###############################################################################
# Read Full Data
###############################################################################
DFS_LIST = [pd.read_csv(f, dtype=splat.STATINK_DTYPES, parse_dates=['period']) for f in FPATHS]
FULL_DF = pd.concat(DFS_LIST)
cols = [i.replace('#', '').strip() for i in list(FULL_DF.columns)]
df = FULL_DF.copy()
###############################################################################
# Make Replacements
###############################################################################
df.columns = cols
df['lobby'] = [splat.LOBBY_MODE[lob] for lob in df['lobby']]
df['mode']  = [splat.GAME_MODE[mod] for mod in df['mode']]


r = re.compile(".*weapon*")
wpnCols = list(filter(r.match, cols))




[Counter(df[i]) for i in wpnCols]

###############################################################################
# Aggregate by date
###############################################################################
df['dummy'] = [1]*df.shape[0]
counts = df.groupby([df['period'].dt.date]).count()['dummy']
(fig, ax) = (plt.figure(), plt.axes())
ax.plot(list(counts))