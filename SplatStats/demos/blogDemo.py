from os import path
import matplotlib.pyplot as plt
import SplatStats as splat


###############################################################################
# Setup paths, username and timezone
###############################################################################
(pName, tz) = ('čħîþ ウナギ', 'America/Los_Angeles')
(iPath, oPath) = (
    path.expanduser('~/Documents/GitHub/s3s/'),
    path.expanduser('./dataBattle/')
)
###############################################################################
# Dump battle objects from JSONs
###############################################################################
hPaths = splat.getDataFilepaths(iPath)
bPaths = splat.dumpBattlesFromJSONS(hPaths, oPath)
###############################################################################
# Instantiate player object
###############################################################################
plyr = splat.Player(pName, bPaths, timezone=tz)
pHist = plyr.battlesHistory
###############################################################################
# Do some filtering!
###############################################################################
filters = (
    pHist['main weapon'] == 'Splattershot',
    pHist['match type'] == 'Turf War',
    pHist['kill'] >= 15,
    pHist['death'] <= 5,
)
fullFilter = [all(i) for i in zip(*filters)]
pHist[fullFilter][['kill', 'head main', 'shirt main', 'shoes main']]
###############################################################################
# Kills/Deaths Histogram
###############################################################################
(fig, ax) = plt.subplots(figsize=(15, 5))
(fig, ax) = splat.plotKillsAndDeathsHistogram(
    (fig, ax), pHist, (0, 40), yRange=(-.25, .25), 
    alpha=.6,
    normalized=True
)
ax.set_ylabel('Density')
ax.set_xlabel('Deaths/Kills')
plt.savefig(
    path.join(oPath, 'KD_Histogram.png'), 
    dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Treemap
###############################################################################
(matchType, metric) = ("Turf War", "paint avg")
if matchType != "All":
    stagesStatsMatch = splat.calcStagesStatsByType(pHist)[matchType]
else:
    stagesDF = splat.calcStagesStats(pHist)
(fig, ax) = plt.subplots(figsize=(5, 5))
(fig, ax) = splat.plotTreemapByStages(
    (fig, ax), stagesDF, metric=metric, 
    fmt='{:.2f}', pad=0.1, alpha=.6
)
ax.set_title(f"{matchType} - {metric}")
plt.savefig(
    path.join(oPath, f'{matchType}-{metric}_Treemap.png'), 
    dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Iris
###############################################################################
(fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
(fig, ax) = splat.plotkillDeathIris(
    (fig, ax), pHist,
    innerGuides=(0, 6, 1), outerGuides=(10, 50, 10),
    frameColor="#000000AA"
)
ax.set_yticklabels(
    ["", 10, 20, 30, 40], 
    fontdict={'fontsize': 8, 'color': '#00000066'}
)
ax.set_rlabel_position(0)
plt.savefig(
    path.join(oPath, 'KD_Iris.png'), 
    dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Match History
###############################################################################
(xRange, yRange) = ((-350, pHist.shape[0]), ((0, 40), (0, 2000)))
fig = plt.figure(figsize=(30, 5))
gs = fig.add_gridspec(
    2, 1,  
    width_ratios=(1, ), height_ratios=(.75, .05),
    left=0.1, right=0.9, bottom=0.1, top=0.9,
    wspace=0.05, hspace=0
)
(ax_top, ax_bottom) = (fig.add_subplot(gs[0]), fig.add_subplot(gs[1], sharex=ax_top))
(_, ax_top) = splat.plotMatchHistory(
    (fig, ax_top), pHist, ilocRange=xRange,
    yRange=yRange, sizeMultiplier=1
)
(_, ax_bottom) = splat.plotMatchTypeHistory(
    (fig, ax_bottom), pHist, ilocRange=xRange,
    sizeMultiplier=.9, labelsize=5.25
)
ax_top.tick_params(labelbottom=False)
ax_bottom.set_yticks([])
plt.setp(ax_bottom.get_xticklabels(), rotation=90, ha='right')
plt.savefig(
    path.join(oPath, 'History.png'), 
    dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor()
)
###############################################################################
# Award BarChart
###############################################################################
awds = plyr.getAwardFrequencies()
(fig, ax) = plt.subplots(figsize=(10, 4))
(fig, ax) = splat.plotAwardFrequencies((fig, ax), awds)
fig.savefig(
    path.join(oPath, 'Awards.png'), 
    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor()
)