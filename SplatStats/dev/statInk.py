
# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

from os import path
from glob import glob
import pandas as pd

DATA_PATH = '/Users/sanchez.hmsc/Downloads/InkStats'
FPATHS = glob(path.join(DATA_PATH, '*-*-*.csv'))


LOBBY_MODE = {
    'regular': 'Regular',
    'bankara_challenge': 'Anarchy (Series)',
    'bankara_open': 'Anarchy (Open)',
    'xmatch': 'X Battle',
    'splatfest_challenge': 'Splatfest (Pro)',
    'splatfest_open': 'Splatfest (Open)'
}
GAME_MODE = {
    'nawabari': 'Turf War',
    'area': 'Splat Zones',
    'yagura': 'Tower Control',
    'hoko': 'Rainmaker',
    'asari': 'Clam Blitz'
}

###############################################################################
# Read Full Data
###############################################################################
DFS_LIST = [pd.read_csv(f, low_memory=False) for f in FPATHS]
FULL_DF = pd.concat(DFS_LIST)
cols = list(FULL_DF.columns)
###############################################################################
# Make Replacements
###############################################################################
df = FULL_DF.copy()
df['lobby'] = [LOBBY_MODE[lob] for lob in df['lobby']]
df['mode']  = [GAME_MODE[lob] for lob in df['mode']]