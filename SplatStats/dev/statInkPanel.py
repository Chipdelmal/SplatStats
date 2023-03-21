# !/usr/bin/env python3

from sys import argv
from glob import glob
from os import path, system
import SplatStats as splat


if splat.isNotebook():
    (six, USR) = (0, 'dsk')
else:
    six = int(argv[1])
SSON = ['Drizzle Season 2022', 'Chill Season 2022', 'Fresh Season 2023']
SEASON = SSON[six]
###############################################################################
# Get files and set font
###############################################################################
if splat.isNotebook():
    if USR=='lab':
        DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
    elif USR=='lap':
        DATA_PATH = '/Users/sanchez.hmsc/Documents/SyncMega/BattlesDocker'
    else:
        DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
else:
    DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
###############################################################################
# Export Panel
###############################################################################
try:
    (bText, rText) = ('Drizzle Season 2022', SEASON)
    fName = path.join(DATA_PATH, 'statInk/'+'InkstatPanel.svg')
    fOutPNG = str(path.join(DATA_PATH, 'statInk/', SEASON+'.png')).replace(' ', '')
    fOutSVG = fOutPNG.replace('.png', '.svg')
    with open(fName, 'r') as file:
        data = file.read()
        data = data.replace(bText, rText)
        data = data.replace(bText.replace(' ', '%20'), rText)
    with open(fOutSVG, 'w') as file:
        file.write(data)
    system(f"inkscape '{fOutSVG}' --export-filename='{fOutPNG}' --export-width=5500")
except:
    pass