
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import SplatStats.constants as cst
import SplatStats.stats as stats


def plotKillsAndDeathsHistogram(
        figAx, playerHistory, killRange, 
        binSize=1, assistsAdjustment=True, normalized=True,
        yRange=(-.25, .25), aspect=.25, alpha=.35, edgecolor='#000000',
        kColor=cst.CLR_KILL_DEATH['kill'], dColor=cst.CLR_KILL_DEATH['death'],
        **kwargs
    ): 
    """Creates a paired histogram in which the top represents player kills, and the bottom the player deaths.
    
    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots)
        playerHistory (dataframe): Player history dataframe with kills, deaths and assists categories.
        killRange (tuple): Minimum and maximum values to consider in the kill or death counts.
        yRange (tuple, optional): Minimum and maximum range values for the y axis in the plot. Defaults to (-.25, .25).
        aspect (float, optional): Aspect ratio of the output plot. Defaults to .25.
        binSize (int, optional): Bin sizes for the frequency counts. Defaults to 1.
        assistsAdjustment (bool, optional): If TRUE, the kills value is calculated as kills+0.5*assists. Defaults to True.
        normalized (bool, optional): If TRUE, the frequencies are divided by the total, so that they add to one. Defaults to True.
        alpha (float, optional): Opacity of the rectangles. Defaults to 0.35.
        kColor (hex, optional): Facecolor for the "kills" rectangles. Defaults to pkg constant.
        dColor (hex, optional): Facecolor for the "deaths" rectangles. Defaults to pkg constant.
        edgecolor (hex, optional): Edgecolor for all the rectangles. Defaults to '#000000'.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    # Calculate frequencies ---------------------------------------------------
    (kills, deaths, assists) = [
        np.array(playerHistory[cat]) for cat in ('kill', 'death', 'assist')
    ]
    if assistsAdjustment:
        kills = kills+0.5*assists
    (kFreqs, dFreqs) = [
        stats.calcBinnedFrequencies(
            arr, killRange[0], killRange[1], 
            binSize=binSize, normalized=normalized
        ) for arr in (kills, deaths)
    ]
    # Generate histogram ------------------------------------------------------
    (fig, ax) = figAx
    # Plot kills
    for (x, k) in enumerate(kFreqs):
        ax.add_patch(
            Rectangle(
                (x, 0), binSize, k, 
                facecolor=kColor, edgecolor=edgecolor,
                alpha=alpha, zorder=0, **kwargs
            )
        )
    # Plot deaths
    for (x, k) in enumerate(dFreqs):
        ax.add_patch(
            Rectangle(
                (x, 0), binSize, -k, 
                facecolor=dColor, edgecolor=edgecolor,
                alpha=alpha, zorder=0, **kwargs
            )
        )
    # Fix axes and return figure
    ax.set_xlim(*killRange)
    ax.set_ylim(*yRange)
    ax.set_aspect(aspect/ax.get_data_ratio())
    return (fig, ax)

