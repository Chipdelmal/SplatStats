
import numpy as np
import SplatStats.stats as stats
import SplatStats.colors as clr


def plotStreamTeam(
        figAx, team, teamHistBT,
        colors=clr.ALL_COLORS,
        metric='kill', normalized=False, smooth=True, 
        smoothness=0.75, gridSize=500, baseline='sym'
    ):
    (fig, ax) = figAx
    # Reshape dataframe and get vars ------------------------------------------
    dfByPlayer = teamHistBT.reorder_levels(["player", "datetime"])
    names = team.names
    entriesNum = dfByPlayer.loc[names[0]].shape[0]
    # Populate stream ---------------------------------------------------------
    stream = np.zeros((len(names), entriesNum))
    for (ix, name) in enumerate(names):
        stream[ix]  = np.array(dfByPlayer.loc[name][metric])
    streamFiltered = stream[:,np.any(stream>0, axis=0)]
    # Normalize if needed -----------------------------------------------------
    if normalized:
        cSum = np.sum(streamFiltered, axis=0)
        streamFiltered = np.array([r/cSum for r in streamFiltered])
    # Plot variables ----------------------------------------------------------
    x = list(range(streamFiltered.shape[1]))
    if smooth:
        smooth = [stats.gaussianSmooth(i, gridSize, smoothness) for i in streamFiltered]
        (x, y) = (smooth[0][0], [i[1] for i in smooth])
    else:
        y = streamFiltered
    # Generate figure ---------------------------------------------------------
    ax.stackplot(x, y, baseline=baseline, colors=colors)
    ax.set_xlim(0, max(x))
    ax.set_xticks([])
    ax.set_yticks([])
    # ax.axis('off')
    ax.legend(
        names, loc='upper left', frameon=False,
        bbox_to_anchor=(1, 1), ncol=2
    )
    return (fig, ax)
