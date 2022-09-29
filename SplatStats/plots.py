
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import SplatStats.constants as cst
import SplatStats.stats as stats
import SplatStats.plotsAux as paux


def plotKillsAndDeathsHistogram(
        figAx, playerHistory, killRange, 
        binSize=1, assistsAdjustment=True, normalized=True,
        yRange=(-.25, .25), aspect=.25, alpha=.35, edgecolor='#000000',
        kColor=cst.CLR_STATS['kill'], dColor=cst.CLR_STATS['death'],
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


def plotMatchTypeHistory(
        figAx, playerHistory,
        labelsize=5, alphaMultiplier=1, sizeMultiplier=1
    ):
    """Plots the matches history strip in terms of match types, win/loss, KO, etc.

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots)
        playerHistory (dataframe): Player history dataframe with kills, deaths and assists categories.
        labelsize (float, optional): Font size for the weapon id ticks labels (use "None" for no label). Defaults to 5.
        alphaMultiplier (int, optional): Multiplier for alpha value of markers. Defaults to 1.
        sizeMultiplier (int, optional): Multiplier for markers size. Defaults to 1.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    (fig, ax) = figAx
    # Retreiving data ---------------------------------------------------------
    (AM, SM) = (alphaMultiplier, sizeMultiplier)
    (PHIST, MNUM) = (playerHistory, playerHistory.shape[0])
    CATS = ('match type', 'win', 'splatfest', 'ko',  'main weapon')
    (mtchType, win, fest, ko, weapon) = [np.array(PHIST[cat]) for cat in CATS]
    # Iterate through matches -------------------------------------------------
    for m in range(MNUM):
        xPos = m
        # Get shapes and colors
        (shapeWL, colorWL) = (cst.MKR_WL[win[m]], cst.CLR_WL[win[m]])
        (shapeMT, colorMT) = (cst.MKR_MT[mtchType[m]], cst.CLR_MT[mtchType[m]])
        (shapeKO, colorKO) = (cst.MKR_KO[ko[m]], cst.CLR_WL[win[m]])
        (shapeFT, colorFT) = (cst.MKR_FEST[fest[m]], cst.CLR_FEST[fest[m]])
        # Plot the elements
        ax.plot(xPos, 0.400, shapeWL, color=colorWL, alpha=0.30*AM, ms=5.00*SM)
        ax.plot(xPos, 0.250, shapeKO, color=colorWL, alpha=0.20*AM, ms=5.00*SM)
        ax.plot(xPos, 0.125, shapeMT, color=colorMT, alpha=0.30*AM, ms=5.00*SM)
        ax.plot(xPos, 0.125, shapeFT, color=colorFT, alpha=0.30*AM, ms=2.50*SM) 
    # Format ax
    # for i in range(0, MNUM, 10):
    #     ax.vlines(
    #         i, 0, 1, 
    #         color='k', ls='--', alpha=.125, lw=.5,
    #         transform=ax.get_xaxis_transform(), zorder=-50
    #     )
    ax.set_xlim(-0.5, MNUM-.5)
    ax.set_ylim(0, .5)
    ax.set_xticks(list(range(MNUM)))
    plt.xticks(rotation=90)
    ax.set_xticklabels(weapon)
    if labelsize:
        ax.tick_params(axis='x', which='major', labelsize=labelsize)
    return (fig, ax)


def plotMatchHistory(
        figAx, playerHistory, yRange=((0, 50), (0, 1750)),
        labelsize=5, alphaMultiplier=1, sizeMultiplier=1
    ):
    (fig, ax) = figAx
    axR = ax.twinx()
    # Retreiving data ---------------------------------------------------------
    (AM, SM) = (alphaMultiplier, sizeMultiplier)
    (PHIST, MNUM) = (playerHistory, playerHistory.shape[0])
    CATS = ('kill', 'death', 'assist', 'special', 'paint')
    (kill, death, assist, special, paint) = [np.array(PHIST[cat]) for cat in CATS]
    CLR_KD = cst.CLR_STATS
    # Main panel ------------------------------------------------------------------
    autoRange = (0, max(max(kill), max(death)))
    (ymin, ymax) = (yRange[0] if yRange else autoRange)
    (yminR, ymaxR) = (yRange[1] if yRange else autoRange)
    for m in range(MNUM):
        xPos = m
        # Kill/Death
        kd = (kill[m]-death[m])
        clr_kd = (CLR_KD['kill'] if kd >= 0 else CLR_KD['death'])
        if kill[m] > 0:
         ax.plot(xPos, kill[m],  cst.MKR_STATS['kill'], color=clr_kd, alpha=0.35, ms=4, zorder=1)
        if death[m] > 0:
            ax.plot(xPos, death[m], cst.MKR_STATS['death'], color=clr_kd, alpha=0.35, ms=4, zorder=1)
        ax.vlines(xPos, kill[m], death[m], color=clr_kd, alpha=0.20, zorder=2)
        # Special/Assist
        if special[m] > 0:
            ax.plot(xPos, special[m], cst.MKR_STATS['special'], color=CLR_KD['special'], alpha=0.1, zorder=0)
        if assist[m] > 0:
            ax.plot(xPos, assist[m], cst.MKR_STATS['assist'], color=CLR_KD['assist'], alpha=0.1, zorder=0)
        # Paint
        axR.plot(xPos, paint[m], '-', color='#ffffff', alpha=0, zorder=0)
        axR.add_patch(Rectangle(
            (xPos-.5, 0), 1, paint[m], 
            facecolor=cst.CLR_PAINT, alpha=.075, zorder=-5
        ))
    for i in range(0, ymax, 10):
        ax.hlines(
            i, 0, 1, 
            color='k', ls='--', alpha=.125, lw=.5,
            transform=ax.get_yaxis_transform(), zorder=-50
        )
    for i in range(0, MNUM, 10):
        ax.vlines(
            i, 0, 1, 
            color='k', ls='--', alpha=.125, lw=.5,
            transform=ax.get_xaxis_transform(), zorder=-50
        )
    ax.set_ylim(ymin, ymax)
    axR.set_ylim(yminR, ymaxR)
    ax.set_xlim(-0.5, MNUM-.5)
    paux.align_yaxis(ax, 0, axR, 0)
    plt.xticks(rotation=90)
    return (fig, ax)