
# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

import re
from os import path
from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import SplatStats as splat

DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/battle-results-csv'
FPATHS = glob(path.join(DATA_PATH, '*-*-*.csv'))

dTypes = {
    '# season': 'string',
    #'period': 'datetime64'
    'game-ver': 'string',
    'lobby': 'string',
    'mode': 'string',
    'stage': 'string',
    'time': 'uint16',
    'rank': 'string',
    'alpha-color': 'string',
    'bravo-color': 'string'
}
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
# Replace weapon names (US standard) ------------------------------------------
for i in range(1, 5):
    df[f'A{i}-weapon'] = [splat.WPNS_DICT[w] for w in df[f'A{i}-weapon']]
    df[f'B{i}-weapon'] = [splat.WPNS_DICT[w] for w in df[f'B{i}-weapon']]
# Replace stages names (US standard) ------------------------------------------
df['stage'] = [splat.STGS_DICT[s] for s in df['stage']]
df['knockout'] = [splat.boolToInt(k) for k in df['knockout']]
nullColor = '#00000000'
df['alpha-color'] = [f'#{c}' if type(c) is str else nullColor for c in df['alpha-color']]
df['bravo-color'] = [f'#{c}' if type(c) is str else nullColor for c in df['bravo-color']]
df['rank'] = [r if type(r) is str else 'NA' for r in df['rank']]


df['power'].unique()

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
df['mode'] = [splat.GAME_MODE[lob] for lob in df['mode']]



###############################################################################
# Testing class
###############################################################################
statInk = splat.StatInk(DATA_PATH)
knocks = [i for i in statInk.battlesResults['knockout'] if (i>=0)]

btls = statInk.battlesResults
alpha = btls[[f'A{i}-weapon' for i in range(1, 5)]]
winrs = btls['win']
bravo = btls[[f'B{i}-weapon' for i in range(1, 5)]]



(vectA, vectE) = (
    DictVectorizer(sparse=False), DictVectorizer(sparse=False)
)

