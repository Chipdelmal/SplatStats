
import numpy as np
from os import path
from sys import argv
import SplatStats as splat
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

if splat.isNotebook():
    (plyrName, weapon, mode, overwrite) = ('čħîþ ウナギ', 'All', 'All', 'True')
    (iPath, bPath, oPath) = (
        path.expanduser('~/Documents/Sync/BattlesDocker/jsons'),
        path.expanduser('~/Documents/Sync/BattlesDocker/battles'),
        path.expanduser('~/Documents/Sync/BattlesDocker/out')
    )
    fontPath = '/home/chipdelmal/Documents/GitHub/SplatStats/other/'
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
title = '(Kills+0.5*Assists)/Deaths'
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
###############################################################################
# Streaks
###############################################################################
wins = list(playerHistory['win'])
splat.longestRun(wins, elem='W')
splat.longestRun(wins, elem='L')
###############################################################################
# Windowed average
###############################################################################
kSize = 8
dHist = splat.aggregateStatsByPeriod(playerHistory, period='2H')
winsArray = np.asarray((dHist['win'])/dHist['matches'])
windowAvg = splat.windowAverage(winsArray, kernelSize=kSize, mode='valid')

(fig, ax) = plt.subplots(figsize=(10, 4))
ax.plot(winsArray, lw=5, color=splat.LUMIGREEN_V_DFUCHSIA_S1[-1], alpha=.15)
ax.plot(
    [i+kSize/2 for i in range(len(windowAvg))], windowAvg,
    lw=4, color=splat.PINK_V_GREEN_S1[0], alpha=.85
)
ax.autoscale(enable=True, axis='x', tight=True)
ax.set_ylim(0, max(winsArray))
###############################################################################
# Circular History
###############################################################################
kassist=True
paint=True
bottomArray=None
barArray=None
tbRange=(0, 55)
bRange=(0, 2500) 
lw=0.3
alpha=1
rScale='symlog'
innerOffset=1.5
clockwise=True
colorsTop=(splat.CLR_STATS['kill'], splat.CLR_STATS['death'])
colorBars=splat.CLR_PAINT
innerText=None
fontSize=20
fontColor="#000000CC"
innerGuides=(0, 6, 1)
innerGuidesColor="#00000066"
outerGuides=(0, 50, 10)
outerGuidesColor="#00000088"
frameColor="#00000011"


mTypeColors = {
    'Clam Blitz':           '#D60E6E',
    'Rainmaker':            '#7D26B5',
    'Splat Zones':          '#3D59DE',
    'Tower Control':        '#8ACF47',
    'Tricolor Turf War':    '#0118E3',
    'Turf War':             '#D1D1D1'
}
winColors = {True: '#6BD52C', False: '#38377A'}
kosColors = {True: '#A714D4', False: '#ffffff'}


(fig, ax) = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
(outer, inner) = (
    np.array(playerHistory['kill']), 
    np.array(playerHistory['death'])
)
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
ax.vlines(
    ANGLES, innerOffset+40, innerOffset+50, 
    lw=lw, colors=[mTypeColors[i] for i in playerHistory['match type']],
    alpha=alpha
)
ax.vlines(
    ANGLES, innerOffset+50, innerOffset+50+5, 
    lw=lw, colors=[winColors[i] for i in playerHistory['winBool']],
    alpha=alpha
)
winKO = []
for wko in list(zip(playerHistory['winBool'], playerHistory['ko'])):
    if wko[-1]:
        if wko[0]:
            winKO.append('#5F0FB4')
        else:
            winKO.append('#E70F21')
    else:
        winKO.append('#ffffff')
ax.vlines(
    ANGLES, innerOffset+40, innerOffset+40-4, 
    lw=lw, colors=winKO,
    alpha=alpha
)
# Draw top-bottom ---------------------------------------------------------
if bottomArray is None:
    bottomArray = np.zeros(topArray.shape)
heights = topArray-bottomArray
colors = [colorsTop[0] if (h>=0) else colorsTop[1] for h in heights]
ax.vlines(
    ANGLES, innerOffset+bottomArray, innerOffset+topArray, 
    lw=lw, colors=colors, alpha=alpha
)
# Draw bar ----------------------------------------------------------------
if barArray is None:
    barScaled = np.zeros(topArray.shape)
else:
    barScaled = np.interp(barArray, bRange, tbRange)
ax.vlines(
    ANGLES, innerOffset, innerOffset+barScaled,  
    lw=1, colors=colorBars, alpha=.025
)
# Add inner text ----------------------------------------------------------
if innerText:
    ax.text(
        x=0.5, y=0.5, 
        s=innerText, fontsize=fontSize,
        va="center", ha="center",  ma="center", 
        color=fontColor, transform=ax.transAxes
    )
# Cleaning up axes --------------------------------------------------------
circleAngles = np.linspace(0, 2*np.pi, 200)
for r in range(*innerGuides):
    ax.plot(
        circleAngles, np.repeat(r+innerOffset, 200), 
        color=innerGuidesColor, lw=0.1, ls='-.', zorder=-10
    )
ax.set_xticks([])
ax.set_xticklabels([])
ax.set_ylim(tbRange[0], tbRange[1]+innerOffset)
ax.set_yticklabels([])
yTicks = [0+innerOffset] + list(np.arange(
    outerGuides[0]+innerOffset, outerGuides[1]+innerOffset, outerGuides[2]
))
ax.set_yticks(yTicks)
ax.yaxis.grid(True, color=outerGuidesColor, ls='-', lw=0.2, zorder=-10)
ax.spines["start"].set_color("none")
ax.spines["polar"].set_color(frameColor)