
# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

from os import path
from glob import glob
import pandas as pd
import numpy as np
import SplatStats as splat

DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/battle-results-csv'
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
DFS_LIST = [pd.read_csv(f, dtype=dTypes, parse_dates=['period']) for f in FPATHS]
FULL_DF = pd.concat(DFS_LIST)
cols = [i.replace('#', '').strip() for i in list(FULL_DF.columns)]
df = FULL_DF.copy()
###############################################################################
# Make Replacements
###############################################################################
df.columns = cols
df['lobby'] = [splat.LOBBY_MODE[lob] for lob in df['lobby']]
df['mode'] = [splat.GAME_MODE[lob] for lob in df['mode']]
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


df['rank'].unique()


###############################################################################
# Testing class
###############################################################################
statInk = splat.StatInk(DATA_PATH)