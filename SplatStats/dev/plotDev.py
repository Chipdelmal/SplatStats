
# import math
# import numpy as np
# from os import path
# from sys import argv
# from matplotlib.patches import Rectangle
# import SplatStats as splat
# import matplotlib.colors as mcolors
# from collections import Counter
# import warnings
# warnings.filterwarnings("ignore")
# import matplotlib.pyplot as plt

# if splat.isNotebook():
#     (plyrName, weapon, mode, overwrite) = ('čħîþ ウナギ', 'All', 'All', 'True')
#     (iPath, bPath, oPath) = (
#         path.expanduser('~/Documents/Sync/BattlesDocker/jsons'),
#         path.expanduser('~/Documents/Sync/BattlesDocker/battles'),
#         path.expanduser('~/Documents/Sync/BattlesDocker/out')
#     )
#     fontPath = '/home/chipdelmal/Documents/GitHub/SplatStats/other/'
# else:
#     (plyrName, weapon, mode, overwrite) = argv[1:]
#     (iPath, bPath, oPath) = (
#         '/data/jsons', 
#         '/data/battles', 
#         '/data/out'
#     )
#     fontPath = '/other/'
# overwrite = (True if overwrite=="True"  else False)
# LEN_LIMIT = 400
# ###############################################################################
# # Auxiliary 
# ###############################################################################
# title = '(Kills+0.5*Assists)/Deaths'
# fNameID = f'{plyrName}-{weapon}'
# splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
# ###############################################################################
# # Process JSON files into battle objects
# ###############################################################################
# hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
# bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=overwrite)
# bFilepaths = splat.getBattleFilepaths(bPath)
# ###############################################################################
# # Create Player Object
# ###############################################################################
# plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
# playerHistory = plyr.battlesHistory
# playerHistory = playerHistory[playerHistory['match mode']!='PRIVATE']
# # Weapon filter ---------------------------------------------------------------
# if weapon != 'All':
#     pHist = playerHistory[playerHistory['main weapon']==weapon]
# else:
#     pHist = playerHistory
# ###############################################################################
# # Streaks
# ###############################################################################
# wins = list(playerHistory['win'])
# splat.longestRun(wins, elem='W')
# splat.longestRun(wins, elem='L')
# ###############################################################################
# # Windowed average
# ###############################################################################
# kSize = 8
# dHist = splat.aggregateStatsByPeriod(playerHistory, period='2H')
# winsArray = np.asarray((dHist['win'])/dHist['matches'])
# windowAvg = splat.windowAverage(winsArray, kernelSize=kSize, mode='valid')

# (fig, ax) = plt.subplots(figsize=(10, 4))
# ax.plot(winsArray, lw=5, color=splat.LUMIGREEN_V_DFUCHSIA_S1[-1], alpha=.15)
# ax.plot(
#     [i+kSize/2 for i in range(len(windowAvg))], windowAvg,
#     lw=4, color=splat.PINK_V_GREEN_S1[0], alpha=.85
# )
# ax.autoscale(enable=True, axis='x', tight=True)
# ax.set_ylim(0, max(winsArray))
###############################################################################
# Circular History
###############################################################################
kassist=True
paint=True
bottomArray=None
barArray=None
tbRange=(0, 60)
bRange=(0, 2500) 
lw=0.25
alpha=1
rScale='symlog'
innerOffset=2
clockwise=True
colorsTop=('#4E4EDDCC', '#CD2D7ECC')
colorBars=splat.CLR_PAINT
innerText=None
fontSize=10
fontColor="#000000CC"
innerGuides=(0, 6, 1)
innerGuidesColor="#00000088"
outerGuides=(0, 50, 10)
outerGuidesColor="#00000088"
frameColor="#00000000"
binMax = 20
binSize = 1
meanStat = True

playerHistory['ink'] = playerHistory['paint']/100
statsHists = {
    i: splat.calcBinnedFrequencies(
        np.array(playerHistory[i]), 0, binMax, binSize=binSize, normalized=True
    )
    for i in ('kill', 'death', 'assist', 'ink', 'special')
}

INKSTATS_STYLE = {
    'kill': {
        'color': '#1A1AAEDD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        'range': (0, 15)
    },
    'death': {
        'color': '#CD2D7EDD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        'range': (0, 15)
    },
    'assist': {
        'color': '#801AB3DD', 'range': (0, 10),
        'scaler': lambda x: np.interp(x, [0, 0.25, 0.65], [0, .70, 0.95]),
        
    },
    'special': {
        'color': '#1FAFE8DD', 'range': (0, 10),
        'scaler': lambda x: np.interp(x, [0, 0.25, 0.65], [0, .70, 0.95]),
    },
    'ink': {
        'color': '#35BA49DD', 'range': (0, 20),
        'scaler': lambda x: np.interp(x, [0, 0.1, 0.2], [0, .70, 0.95]),
    }
}

mTypeColors = {
    'Clam Blitz':           '#D60E6E',
    'Rainmaker':            '#7D26B5',
    'Splat Zones':          '#3D59DE',
    'Tower Control':        '#8ACF47',
    'Tricolor Turf War':    '#E70F21',
    'Turf War':             '#D1D1D1'
}
winColors = {True: '#6BD52C', False: '#D1D1D1'}
kosColors = {True: '#A714D4', False: '#ffffff'}


(fig, ax) = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
(outer, inner) = (np.array(playerHistory['kill']), np.array(playerHistory['death']))
if kassist:
    outer = outer + (.5 * np.array(playerHistory['assist']))
bar = (np.array(playerHistory['paint']) if paint else None)
if innerText:
    text = np.sum(outer)/np.sum(inner)

(topArray, bottomArray, barArray) = (outer, inner, bar)
ax.set_theta_offset(np.pi/2)
ax.set_rscale(rScale)
# Calculate angles for marker lines ---------------------------------------
DLEN = topArray.shape[0]
(astart, aend) = ((2*np.pi, 0) if clockwise else (0, 2*np.pi))
ANGLES = np.linspace(astart, aend, DLEN, endpoint=False)
# Match type --------------------------------------------------------------
(mTypeOff, mTypeHeight) = (40, 8)
(wBoolOff, wBoolHeight) = (mTypeOff+mTypeHeight+2, mTypeOff+mTypeHeight+5)
(kBoolOff, kBoolHeight) = (mTypeOff+mTypeHeight+5, mTypeOff+mTypeHeight+7)
ax.vlines(
    ANGLES, innerOffset+mTypeOff, innerOffset+mTypeOff+mTypeHeight, 
    lw=lw, colors=[mTypeColors[i] for i in playerHistory['match type']],
    alpha=alpha, zorder=-5
)
ax.vlines(
    ANGLES, wBoolOff, wBoolHeight, 
    lw=lw, colors=[winColors[i] for i in playerHistory['winBool']],
    alpha=alpha, zorder=-5
)
winKO = []
for wko in list(zip(playerHistory['winBool'], playerHistory['ko'])):
    if wko[-1]:
        if wko[0]:
            winKO.append('#311AA8')
        else:
            winKO.append('#E70F21')
    else:
        winKO.append('#ffffff')
ax.vlines(
    ANGLES, kBoolOff, kBoolHeight, 
    lw=lw, colors=winKO,
    alpha=alpha, zorder=-5
)
# Vspan for stats ---------------------------------------------------------
STATS = ('kill', 'death', 'assist', 'ink', 'special', )
binsNum = statsHists['kill'].shape[0]
(dHeight, rWidth) = (0.1, 2*math.pi/binsNum)
statsNames = list(STATS)
# Iterate through stats
for (ix, stat) in enumerate(statsNames):
    # Iterate through bins
    (clr, sca) = (
        mcolors.ColorConverter().to_rgba(INKSTATS_STYLE[stat]['color']),
        INKSTATS_STYLE[stat]['scaler']
    )
    bins = statsHists[stat]
    for (jx, h) in enumerate(range(binsNum)):
        alpha = sca(bins[jx])
        ax.add_patch(
            Rectangle(
                (-jx*rWidth, innerOffset-ix*dHeight), -rWidth, -dHeight,
                facecolor=(clr[0], clr[1], clr[2], alpha),
                edgecolor='#00000033', lw=0.1
            )
        )
# Quantiles ---------------------------------------------------------------
statQNT = {s: np.quantile(playerHistory[s], [0.25, 0.50, 0.75]) for s in STATS}
statMNS = {s: np.mean(playerHistory[s]) for s in STATS}
for (ix, stat) in enumerate(statsNames):
    if meanStat:
        rPos = np.interp(statMNS[stat], [0, binMax], [2*math.pi, 0])
        ax.vlines(
            rPos, 
            innerOffset-(ix)*dHeight, innerOffset-(1+ix)*dHeight,  
            lw=.5, colors='#00000099'
        )
    else:
        rPos = [
            np.interp(x, [0, binMax], [2*math.pi, 0])-rWidth/2
            for x in statQNT[stat]
        ]
        ax.vlines(
            rPos[1], 
            innerOffset-(ix)*dHeight, innerOffset-(1+ix)*dHeight,  
            lw=.5, colors='#00000099'
        )
        ax.vlines(
            [rPos[0], rPos[-1]], 
            innerOffset-(ix)*dHeight, innerOffset-(1+ix)*dHeight,  
            lw=.1, colors='#00000000'
        )
# Draw top-bottom ---------------------------------------------------------
if bottomArray is None:
    bottomArray = np.zeros(topArray.shape)
heights = topArray-bottomArray
colors = [colorsTop[0] if (h>=0) else colorsTop[1] for h in heights]
ax.vlines(
    ANGLES, innerOffset+bottomArray, innerOffset+topArray, 
    lw=lw, colors=colors
)
# Draw bar ----------------------------------------------------------------
if barArray is None:
    barScaled = np.zeros(topArray.shape)
else:
    barScaled = np.interp(barArray, bRange, tbRange)
ax.vlines(
    ANGLES, innerOffset, innerOffset+barScaled,  
    lw=lw, colors=colorBars, alpha=.1
)
# Add inner text ----------------------------------------------------------
(kill, death, assist, paint, special) = (
    [np.sum(playerHistory['kill']), np.mean(playerHistory['kill'])],
    [np.sum(playerHistory['death']), np.mean(playerHistory['death'])],
    [np.sum(playerHistory['assist']), np.mean(playerHistory['assist'])],
    [np.sum(playerHistory['paint']), np.mean(playerHistory['paint'])],
    [np.sum(playerHistory['special']), np.mean(playerHistory['special'])],
)
# np.quantile(playerHistory['kill'], [0.25, 0.5, 0.75])
winNum = np.sum(playerHistory['winBool'])
winRate = winNum/DLEN
(sw, sl) = (splat.longestRun(wins, elem='W'), splat.longestRun(wins, elem='L'))
strLng = 'Matches: {}\nWin: {} ({:.2f}%)\nLongest Streaks: W{}-L{}\n\n\n\n\nKill: {} ({:.2f})\nAssist: {} ({:.2f})\nDeath: {} ({:.2f})\nPaint: {} ({:.2f})'
innerText = strLng.format(
    DLEN, winNum, winRate*100, sw, sl,
    kill[0], kill[1], assist[0], assist[1], death[0], death[1], paint[0], paint[1]
)
ax.text(
    x=0.5, y=0.5, 
    s=innerText, fontsize=fontSize,
    va="center", ha="center",  ma="center", 
    color=fontColor, transform=ax.transAxes
)
ax.text(
    x=0.5, y=0.5,
    s='{}'.format(plyrName),
    fontsize=fontSize+7.5,
    va="center", ha="center",  ma="center", 
    color=fontColor, transform=ax.transAxes
)
# Cleaning up axes --------------------------------------------------------
ax.vlines(
    np.arange(aend, astart, (astart+aend)/32), innerOffset, innerOffset+mTypeOff,  
    lw=0.2, colors='#000000', alpha=1, zorder=10
)
ax.vlines(
    [0], innerOffset-dHeight*len(STATS), innerOffset+mTypeOff, 
    lw=0.25, color='#000000CC',
    zorder=10
)
circleAngles = np.linspace(0, 2*np.pi, 200)
for r in range(*innerGuides):
    ax.plot(
        circleAngles, np.repeat(r+innerOffset, 200), 
        color=innerGuidesColor, lw=0.1, # ls='-.', 
        zorder=10
    )
ax.plot(
    circleAngles, np.repeat(innerOffset-dHeight*len(STATS), 200), 
    color='#000000FF', lw=0.25, # ls='-.', 
    zorder=10
)
ax.set_xticks([])
ax.set_xticklabels([])
ax.set_ylim(tbRange[0], tbRange[1]+innerOffset)
ax.set_yticklabels([])
yTicks = [0+innerOffset] + list(np.arange(
    outerGuides[0]+innerOffset, outerGuides[1]+innerOffset, outerGuides[2]
))
ax.set_yticks(yTicks)
ax.yaxis.grid(True, color=outerGuidesColor, ls='-', lw=0.2, zorder=10)
ax.spines["start"].set_color("none")
ax.spines["polar"].set_color(frameColor)
fig.savefig(
    path.join(oPath, f'DemoIris.png'), 
    dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor()
)