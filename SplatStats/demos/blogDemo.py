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
    innerGuides=(0, 6, 1), outerGuides=(10, 50, 10)
)