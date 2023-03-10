# !/usr/bin/env python3

# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

import fileinput
from os import path, system
from glob import glob
import pandas as pd
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
from colour import Color
from matplotlib.ticker import EngFormatter
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import SplatStats as splat
import chord as chd


USR='lab'
# ['Drizzle Season 2022', 'Chill Season 2022', 'Fresh Season 2023']
SEASON = 'Fresh Season 2023'
TOP = 20
###############################################################################
# Get files and set font
###############################################################################
if USR=='lab':
    DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
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
# Frequency Analysis
###############################################################################
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
# Calculating totals ----------------------------------------------------------
(totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
totalM = totalW + totalL
wpnsTriplets = zip(names, totalM, totalW, totalL)
wpnSortZip = zip(totalM, wpnsTriplets)
wpnsDict = {x[0]: (x[1], x[2], x[3]) for (_, x) in sorted(wpnSortZip)[::]}
wlRatio = [i[1]/i[0] for i in wpnsDict.values()]
# Polar barchart --------------------------------------------------------------
nItems = len(wlRatio)
itr = zip(
    [nItems-i for i in range(nItems)], 
    wpnsDict.keys(), 
    wlRatio
)
labels = ['{:02d}. {} ({}%)'.format(ix, n, int(f*100)) for (ix, n, f) in itr]
COLORS = splat.ALL_COLORS
shuffle(COLORS)
(fig, ax) = plt.subplots(
    figsize=(12, 12), subplot_kw={"projection": "polar"}
)
(fig, ax) = splat.polarBarChart(
    labels, [i[0] for i in wpnsDict.values()],
    yRange=(0, 1e6), rRange=(0, 180), ticksStep=4,
    colors=[c+'DD' for c in COLORS],
    edgecolor='#00000088', linewidth=0,
    figAx=(fig, ax),
    ticksFmt={
        'lw': 1, 'range': (-.2, 1), 
        'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.1e}'
    },
    labelFmt={
        'color': '#000000EE', 'fontsize': 4.25, 
        'ha': 'left', 'fmt': '{:.1f}'
    }
)
# formatter1 = EngFormatter(places=1, unit="", sep="")
# ax.xaxis.set_major_formatter(formatter1)
xlabels = ax.get_xticklabels()
for txt in xlabels:
    lab = txt.get_text()
    txt.set_text('{:.2f}M'.format(float(lab)/1e6))
# labels[0].set_text('')
ax.set_xticklabels(xlabels, rotation=0, fontsize=7.5)
fName = 'Polar - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Type of Lobby
###############################################################################
cntr = Counter(btlsFiltered['lobby'])
# Generate lobby barchart -----------------------------------------------------
(fig, ax) = plt.subplots(figsize=(0.4, 20))
(series, data) = (list(cntr.keys()), [[int(i)] for i in list(cntr.values())])
data = [[i[0]/1000] for i in data]
(fig, ax) = splat.plotStackedBar(
    data, series, 
    labels=[i.replace(' ', '\n') for i in list(cntr.keys())],
    figAx=(fig, ax),
    category_labels=False, 
    show_values=True, 
    value_format="{:.0f}k",
    colors=[
        '#2E0CB5', '#B400FF', '#6BFF00', '#525CF5', '#FDFF00', '#D01D79'
    ],
    fontsize=8.5, xTickOffset=0.7
)
ax.axis('off')
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.text(
    -2.25, 0.5, 'Total matches: {:.0f}k'.format(np.sum(data)),
    fontsize=20,
    horizontalalignment='center',
    verticalalignment='center',
    transform=ax.transAxes,
    rotation=90
)
fName = 'StackedLobby - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Stacked Barchart
###############################################################################
btlsFiltered['dummy'] = [1]*btlsFiltered.shape[0]
gModes = sorted(list(btlsFiltered['mode'].unique()))
counts = []
for gMode in gModes:
    fltrs = (btlsFiltered['mode']==gMode, )
    fltrBool = [all(i) for i in zip(*fltrs)]
    btlsMode = btlsFiltered[fltrBool]
    c = btlsMode.groupby([btlsMode['period'].dt.date]).count()['dummy']
    c.name = gMode
    counts.append(c)
df = pd.DataFrame(counts).fillna(0).T
df.sort_index(inplace=True)
xys = [
    splat.gaussianSmooth(list(df[gm]), gridSize=1000, sd=0.75) for gm in gModes
]
x = xys[0][0]
(fig, ax) = (plt.figure(figsize=(20, 5)), plt.axes())
ax.stackplot(
    xys[0][0], *[-y[1] for y in xys], 
    labels=gModes, baseline='zero',
    colors=['#DE0B64', '#FFFF00', '#525CF5', '#6BFF00', '#311AA8']
)
ax.legend(loc='upper left').remove()
ax.set_xlim(0, x[-1])
ax.set_ylim(0, -1250)
xtickRan = np.arange(0, x[-1], 15)
ax.set_ylim(ax.get_ylim()[::-1])
ax.xaxis.tick_top()
ax.set_xticks(
    xtickRan, 
    ['{}/{}'.format(df.index[i].month, df.index[i].day) for i in xtickRan],
    ha='left', va='bottom', rotation=0,
    fontsize=12.5
)
ax.set_yticks([], [])
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
fName = 'Stacked - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Frequency Analysis
###############################################################################
RAN = 300e3
COLORS = [c+'DD' for c in splat.ALL_COLORS]
# Iterate through modes -------------------------------------------------------
gModes = sorted(list(btlsFiltered['mode'].unique()))
gMode = gModes[0]
for gMode in gModes:
    shuffle(COLORS)
    fltrs = (btlsFiltered['mode']==gMode, )
    fltrBool = [all(i) for i in zip(*fltrs)]
    btlsMode = btlsFiltered[fltrBool]
    (names, matrix) = splat.calculateDominanceMatrixWins(btlsMode)
    # Calculating totals ------------------------------------------------------
    (totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
    totalM = totalW + totalL
    wpnsTriplets = zip(names, totalM, totalW, totalL)
    wpnSortZip = zip(totalM, wpnsTriplets)
    wpnsDict = {x[0]: (x[1], x[2], x[3]) for (_, x) in sorted(wpnSortZip)[::]}
    wlRatio = [i[1]/i[0] for i in wpnsDict.values()]
    # Assembling tops ---------------------------------------------------------
    topWeapons = [(k, wpnsDict[k]) for k in list(wpnsDict)[-TOP:]][::-1]
    totPart = np.sum(totalM)  
    ###########################################################################
    # Polar Barchart Plot
    ###########################################################################
    nItems = len(wlRatio)
    itr = zip(
        [nItems-i for i in range(nItems)], 
        wpnsDict.keys(), 
        wlRatio
    )
    labels = ['{:02d}. {} ({}%)'.format(ix, n, int(f*100)) for (ix, n, f) in itr]
    COLORS = splat.ALL_COLORS
    shuffle(COLORS)
    (fig, ax) = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})
    (fig, ax) = splat.polarBarChart(
        [f'{TOP-ix:02d}. {wp[0]}  ' for (ix, wp) in enumerate(topWeapons[::-1])], 
        [v[1][0] for v in topWeapons[::-1]],
        yRange=(0, RAN), rRange=(0, 90), ticksStep=1,
        colors=[c+'DD' for c in COLORS], direction=1,
        edgecolor='#00000088', linewidth=0,
        figAx=(fig, ax),
        ticksFmt={
            'lw': 1, 'range': (-.2, 1), 
            'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.1e}'
        },
        labelFmt={
            'color': '#000000EE', 'fontsize': 12, 
            'ha': 'left', 'fmt': '{:.1f}'
        }
    )
    xlabels = ax.get_xticklabels()
    for txt in xlabels:
        lab = txt.get_text()
        txt.set_text('{:.0f}k'.format(float(lab)/1e3))
    xlabels[0] = ''
    ax.set_xticklabels(xlabels, rotation=0, fontsize=12.5)
    fName = 'GMFrequencyPolar {} - {}.png'.format(gMode, SEASON)
    ax.text(
        0.5, 0.48, 
        '{} (participation: {:.2f}M)'.format(gMode, totPart/1e6),
        fontsize=20,
        horizontalalignment='right',
        verticalalignment='top',
        rotation=0,
        transform=ax.transAxes
    )
    plt.savefig(
        path.join(DATA_PATH, 'statInk/'+fName),
        dpi=350, transparent=False, facecolor='#ffffff', 
        bbox_inches='tight'
    )
    plt.close('all')
    ###########################################################################
    # Regular Barchart Plot
    ###########################################################################
    (fig, ax) = plt.subplots(figsize=(18, 8))
    (ix, parPart, delta) = (0, [], 0.5)
    for (wpn, twl) in topWeapons:
        (t, w, l) = twl
        b = ax.barh(
            delta*(len(topWeapons)-ix), t, 
            height=delta*0.95, color=COLORS[ix]
        )
        parPart.append(t/totPart)
        ix=ix+1
    ax.set_yticks(
        delta*np.arange(1, TOP+1), 
        labels=[
            '{} ({:.2f}%)'.format(lab[0], ix*100) 
            for (ix, lab) in zip(parPart[::-1], topWeapons[::-1])
        ],
        fontsize=13.5,
        rotation=45,
        ha='right', ma='right'
    )
    ax.set_xlim(0, RAN)
    ax.set_ylim(delta*0.5, delta*(TOP+.5))
    labels = [int(item.get_text())/1000 for item in ax.get_xticklabels()]
    labelsFix = [f'{i:.0f}k' for i in labels]
    labelsFix[0] = ''
    ax.set_xticklabels(labelsFix)
    plt.xticks(rotation=45, ha='right', fontsize=20)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.text(
        RAN, TOP*delta+delta, 
        'Total Participation: {:.2f}M'.format(totPart/1e6),
        fontsize=20,
        horizontalalignment='center',
        verticalalignment='top',
        rotation=90
    )
    fName = 'GMFrequency {} - {}.png'.format(gMode, SEASON)
    plt.savefig(
        path.join(DATA_PATH, 'statInk/'+fName),
        dpi=350, transparent=False, facecolor='#ffffff', 
        bbox_inches='tight'
    )
    plt.close('all')
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
