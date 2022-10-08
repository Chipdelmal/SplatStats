
import math
import squarify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import SplatStats.constants as cst
import SplatStats.stats as stats
import SplatStats.plotsAux as paux
import matplotlib
matplotlib.rcParams['font.family'] = ['monospace']
# matplotlib.rcParams['font.stretch'] = ['condensed']


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
        labelsize=5, alphaMultiplier=1, sizeMultiplier=1,
        ilocRange=(0, -1)
    ):
    """Plots the matches history strip in terms of match types, win/loss, KO, etc.

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        playerHistory (dataframe): Player history dataframe with kills, deaths and assists categories.
        labelsize (float, optional): Font size for the weapon id ticks labels (use "None" for no label). Defaults to 5.
        alphaMultiplier (int, optional): Multiplier for alpha value of markers. Defaults to 1.
        sizeMultiplier (int, optional): Multiplier for markers size. Defaults to 1.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """
    playerHistory = playerHistory.iloc[ilocRange[0]:ilocRange[1]] 
    # Generate figure ---------------------------------------------------------   
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
        labelsize=6, alphaMultiplier=1, sizeMultiplier=1,
        printStats=True, ilocRange=(0, -1)
    ):
    """Generates a scatter plot of all the matches, and provides information on kills, deaths, paint, assists, specials, etc. Please refer to our website for more information.

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        playerHistory (dataframe): Player history dataframe with kills, deaths and assists categories.
        yRange (tuple, optional): _description_. Defaults to ((0, 50), (0, 1750)).
        labelsize (float, optional): Font size for stats legend. Defaults to 5.
        alphaMultiplier (int, optional): Unused. Defaults to 1.
        sizeMultiplier (int, optional): Unused. Defaults to 1.
        printStats (bool, optional): If False, no stats legend boxes are added to the plot. Defaults to True.
    
    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """
    pStats = stats.calcBattleHistoryStats(playerHistory)
    playerHistory = playerHistory.iloc[ilocRange[0]:ilocRange[1]]
    # Generate figure ---------------------------------------------------------     
    (fig, ax) = figAx
    axR = ax.twinx()
    # Retreiving data ---------------------------------------------------------
    (AM, SM) = (alphaMultiplier, sizeMultiplier)
    (PHIST, MNUM) = (playerHistory, playerHistory.shape[0])
    CATS = ('kill', 'death', 'assist', 'special', 'paint')
    (kill, death, assist, special, paint) = [np.array(PHIST[cat]) for cat in CATS]
    CLR_KD = cst.CLR_STATS
    # Main panel --------------------------------------------------------------
    autoRange = (0, max(max(kill), max(death)))
    (ymin, ymax) = (yRange[0] if yRange else autoRange)
    (yminR, ymaxR) = (yRange[1] if yRange else autoRange)
    for m in range(MNUM):
        xPos = m
        # Kill/Death
        kd = (kill[m]-death[m])
        clr_kd = (CLR_KD['kill'] if kd >= 0 else CLR_KD['death'])
        if kill[m] > 0:
            ax.plot(
                xPos, kill[m],  cst.MKR_STATS['kill'], 
                color=clr_kd, alpha=0.35, ms=4*SM, zorder=1
            )
        if death[m] > 0:
            ax.plot(
                xPos, death[m], cst.MKR_STATS['death'], 
                color=clr_kd, alpha=0.35, ms=4*SM, zorder=1
            )
        ax.vlines(xPos, kill[m], death[m], color=clr_kd, alpha=0.20, zorder=2)
        # Special/Assist
        if special[m] > 0:
            ax.plot(
                xPos, special[m], cst.MKR_STATS['special'], 
                color=CLR_KD['special'], ms=3*SM, alpha=0.1, zorder=0
            )
        if assist[m] > 0:
            ax.plot(
                xPos, assist[m], cst.MKR_STATS['assist'], 
                color=CLR_KD['assist'], ms=3*SM, alpha=0.1, zorder=0
            )
        # Paint
        axR.plot(xPos, paint[m], '-', color='#ffffff', alpha=0, zorder=0)
        axR.add_patch(Rectangle(
            (xPos-.5, 0), 1, paint[m], 
            facecolor=cst.CLR_PAINT, alpha=.05, zorder=-5
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
    # Stats -------------------------------------------------------------------
    (mNum, wratio, kratio, win, loss, aratio) = [
        pStats['general'][i] 
        for i in (
            'total matches', 'win ratio', 'kill ratio', 
            'win', 'loss', 'kassists ratio'
        )
    ]
    (kNum, dNum, aNum, kaNum) = [
        pStats['kpads'][i] 
        for i in ('kills', 'deaths', 'assists', 'kassists')
    ]
    (kAvg, dAvg, aAvg, kaAvg, pAvg) = [
        pStats['kpads avg'][i] 
        for i in ('kills', 'deaths', 'assists', 'kassists', 'paint')
    ]
    (kpm, dpm, apm, kapm, ppm) = [
        pStats['kpads per min'][i] 
        for i in ('kills', 'deaths', 'assists', 'kassists', 'paint')
    ]
    paint = pStats['general']['paint']
    # Text
    sStr = f'''{wratio:.2f} W/L ({win:04d}/{loss:04d}) 
               {kratio:.2f} K/D ({kNum:04d}/{dNum:04d}) 
               {aratio:.2f} A/D ({int(kaNum):04d}/{dNum:04d}) 
            '''.expandtabs()
    mStr = f''' Matches:  {mNum:06d}  ( avg  &  pmin)
 Paint:    {paint:06d}  ({pAvg:.1f} & {ppm:.1f})
 Kills:    {kNum:06d}  ({kAvg:.3f} & {kpm:.3f})
 Deaths:   {dNum:06d}  ({dAvg:.3f} & {dpm:.3f})
 Assists:  {aNum:06d}  ({aAvg:.3f} & {apm:.3f})
 KAssists: {int(kaNum):06d}  ({kaAvg:.3f} & {kapm:.3f})
        '''.expandtabs()
    if printStats:
        ax.text(
            1, .99, sStr, fontsize=labelsize,
            horizontalalignment='right', verticalalignment='top',
            transform=ax.transAxes
        )
        ax.text(
            0, .99, mStr, fontsize=labelsize,
            horizontalalignment='left', verticalalignment='top',
            transform=ax.transAxes
        )
    # Axes --------------------------------------------------------------------
    ax.set_ylim(ymin, ymax)
    axR.set_ylim(yminR, ymaxR)
    ax.set_xlim(-0.5, MNUM-.5)
    paux.align_yaxis(ax, 0, axR, 0)
    plt.xticks(rotation=90)
    return (fig, ax)


def generateMatchHistoryLegend(figAx):
    """Creates a legend with the breakdown of the Match History plots.

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    (fig, ax) = figAx
    # Generate dummy figure for handles ---------------------------------------
    (figD, axD) = plt.subplots(figsize=(1, .5))
    for (ix, k) in enumerate(cst.MKR_STATS.keys()):
        axD.plot(
            0, 0, cst.MKR_STATS[k], 
            color=cst.CLR_STATS[k], label=k, alpha=.5
        )
    for (ix, k) in enumerate(cst.MKR_WL.keys()):
        axD.plot(
            0, 0, cst.MKR_WL[k], 
            color=cst.CLR_WL[k], label=k, alpha=.5
        )
    ko = ('KO Win', 'KO Loss')
    for (ix, k) in enumerate(cst.MKR_KO.keys()):
        axD.plot(
            0, 0, cst.MKR_KO[True], 
            color=list(cst.CLR_WL.values())[ix], label=ko[ix], alpha=.5
        )
    for (ix, k) in enumerate(cst.MKR_MT.keys()):
        axD.plot(
            0, 0, cst.MKR_MT[k], 
            color=cst.CLR_MT[k], label=k, alpha=.5
        )
    for (ix, k) in enumerate((True, )):
        axD.plot(
            0, 0, cst.MKR_FEST[k], 
            color=cst.CLR_FEST[k], label='Splatfest', alpha=.5, ms=2
        )
    # Add legend from dummy figure --------------------------------------------
    # (figL, axL) = plt.subplots(figsize=(1, 5))
    ax.legend(*axD.get_legend_handles_labels(), frameon=False)
    ax.axis('off')
    # Close dummy image and return legend -------------------------------------
    plt.close(figD)
    return (fig, ax)


def plotTreemapByStages(
        figAx, stagesDF, 
        metric='win ratio', fmt='{:.2f}', title=True,
        pad=0.1, lw=2, ec='#00000055', alpha=.5
    ):
    """_summary_

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        stagesDF (dataframe): Stage statistics dataframe (see "calcStagesStats" or "calcStagesStatsByType").
        metric (str, optional): Metric of the dataframe that will be plotted (column). Defaults to 'win ratio'.
        fmt (str, optional): Format string for the numbers labels. Defaults to '{:.2f}'.
        pad (int, optional): Padding in-between rectangles. Defaults to 0.
        lw (int, optional): Rectangle line width. Defaults to 2.
        ec (str, optional): Rectangle line color. Defaults to '#00000055'.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """
    stages = stagesDF['stage']
    colors = [cst.CLR_STAGE[s] for s in stages]
    (fig, ax) = plotTreemapByKey(
        figAx, stagesDF, key='stage',
        metric=metric, fmt=fmt, title=title,
        pad=pad, lw=lw, ec=ec, alpha=alpha, colors=colors
    )
    return (fig, ax)


def plotTreemapByKey(
        figAx, keyedDF, key,
        metric='win ratio', fmt='{:.2f}', title=True,
        pad=0.1, lw=2, ec='#00000055', alpha=.5,
        colors=cst.CLR_CLS_LONG
    ):
    """_summary_

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        keyedDF (dataframe): Key-statistics dataframe (see "calcStagesStatsByType").
        metric (str, optional): Metric of the dataframe that will be plotted (column). Defaults to 'win ratio'.
        fmt (str, optional): Format string for the numbers labels. Defaults to '{:.2f}'.
        pad (int, optional): Padding in-between rectangles. Defaults to 0.
        lw (int, optional): Rectangle line width. Defaults to 2.
        ec (str, optional): Rectangle line color. Defaults to '#00000055'.
        colors (lst, optional): List of colors in order of appearance. Defailts to cst.CLR_CLS_LONG.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    # Filter out rows that would have 0 area (error) --------------------------
    keyedDF = keyedDF[keyedDF[metric] > 0]
    values = keyedDF[metric]
    stages = list(keyedDF[key])
    # Generate treemap --------------------------------------------------------
    (fig, ax) = figAx
    ax = squarify.plot(
        sizes=values, 
        alpha=alpha,
        value=[fmt.format(s) for s in values],
        color=colors,
        pad=pad, bar_kwargs={
            'edgecolor': ec, 'linewidth': lw, 
            'capstyle': 'round', 'capsize': 2
        }
    )
    labels = [f"{s} ("+(fmt.format(v))+")" for (s, v) in zip(stages, values)]
    plt.legend(
        handles=ax.containers[0], 
        labels=labels,
        loc='upper left',
        bbox_to_anchor=(1, 1),
        ncol=1,
        framealpha=0,
        fontsize=12
    )
    if title:
        plt.title(metric)
    ax.set_aspect(1/ax.get_data_ratio())
    plt.axis('off')
    return (fig, ax)


def plotIris(
        figAx, 
        topArray, bottomArray=None, barArray=None, 
        tbRange=(0, 50), bRange=(0, 2000),
        rScale='symlog', innerOffset=0.75, clockwise=True,
        colorsTop=(cst.CLR_STATS['kill'], cst.CLR_STATS['death']),
        colorBars=cst.CLR_PAINT,
        innerText=None, fontSize=20, fontColor='#00000066',
        innerGuides=(0, 6, 1), innerGuidesColor="#00000066",
        outerGuides=(0, 50, 5), outerGuidesColor="#00000088",
        frameColor="#00000011"
    ):
    """Creates a barchart-style plot in a radial axis. The lines go from bottomArray to topArray, while the barArray is plotted as is from the origin.

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        topArray (array):
        bottomArray (array, optional):
        barArray (array, optional):
        tbRange (tuple, optional): y-range for the top-bottom radii. Defaults to (0, 50).
        bRange (tuple, optional): y-range for the bar statistic. Defaults to (0, 2000).
        rScale (str, optional): Way the circular axis will be scaled. Defaults to 'symlog'.
        innerOffset (float, optional): Radius of the innermost circle to create a clear area at the centar of the plot. Defaults to 0.75.
        clockwise (bool, optional): Sorting of the battles starts at 12 o'clock and goes clockwise. Defaults to True.
        colorsTop (tuple, optional): Color of the line if kills are larger than deaths, and if they are not. Defaults to (cst.CLR_STATS['kill'], cst.CLR_STATS['death']).
        colorBars (color, optional): Color of the bars assigned to the paint statistic. Defaults to cst.CLR_PAINT.
        innerText (bool, optional): Add the inner label as the ratio of kills or kassists to deaths. Defaults to True.
        innerTextFmt (str, optional): Formatting string for the inner label. Defaults to '{:.2f}'.
        fontSize (int, optional): Font size for the inner label. Defaults to 20.
        fontColor (str, optional): Font color for the inner label. Defaults to '#00000066'.
        innerGuides (tuple, optional): Start, stop, increment values for the innermost guides on the radial axis. Defaults to (0, 6, 1).
        innerGuidesColor (str, optional): Color for the innermost guides. Defaults to "#00000066".
        outerGuides (tuple, optional): Start stop, increment values for the outermost guides on the radial axis. Defaults to (0, 50, 10).
        outerGuidesColor (str, optional): Color for the outer guides. Defaults to "#00000088".
        frameColor (str, optional): Color for the outermost radial frame. Defaults to "#00000011".

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    (fig, ax) = figAx
    ax.set_theta_offset(np.pi/2)
    ax.set_rscale(rScale)
    # Calculate angles for marker lines ---------------------------------------
    DLEN = topArray.shape[0]
    (astart, aend) = ((2*np.pi, 0) if clockwise else (0, 2*np.pi))
    ANGLES = np.linspace(astart, aend, DLEN, endpoint=False)
    # Draw top-bottom ---------------------------------------------------------
    if bottomArray is None:
        bottomArray = np.zeros(topArray.shape)
    heights = topArray-bottomArray
    colors = [colorsTop[0] if (h>=0) else colorsTop[1] for h in heights]
    ax.vlines(
        ANGLES, innerOffset+bottomArray, innerOffset+topArray, 
        lw=0.5, colors=colors, alpha=.7
    )
    # Draw bar ----------------------------------------------------------------
    if barArray is None:
        barScaled = np.zeros(topArray.shape)
    else:
        barScaled = np.interp(barArray, bRange, tbRange)
    ax.vlines(
        ANGLES, innerOffset, innerOffset+barScaled,  
        lw=1, colors=colorBars, alpha=.1
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
    ax.set_ylim(tbRange[0], tbRange[1]+innerOffset)
    ax.set_yticklabels([])
    yTicks = [0+innerOffset] + list(np.arange(
        outerGuides[0]+innerOffset, outerGuides[1]+innerOffset, outerGuides[2]
    ))
    ax.set_yticks(yTicks)
    ax.yaxis.grid(True, color=frameColor, ls='-', lw=0.125, zorder=-10)
    ax.spines["start"].set_color("none")
    ax.spines["polar"].set_color(outerGuidesColor)
    # Return figure -----------------------------------------------------------
    return (fig, ax)


def plotkillDeathIris(
        figAx, playerHistory, kassist=True, paint=True,
        kRange=(0, 50), pRange=(0, 2000),
        rScale='symlog', innerOffset=0.75, clockwise=True,
        colorsTop=(cst.CLR_STATS['kill'], cst.CLR_STATS['death']),
        colorBars=cst.CLR_PAINT,
        innerText=True, innerTextFmt='{:.2f}',
        fontSize=20, fontColor='#00000066',
        innerGuides=(0, 6, 1), innerGuidesColor="#00000066",
        outerGuides=(0, 50, 10), outerGuidesColor="#00000088",
        frameColor="#00000011"
    ):
    """These plots show the kill to death ratios as bars arranged in a circular pattern.

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        playerHistory (dataframe): Player history dataframe with kills, deaths and assists categories.
        kassist (bool, optional): Combine the kill and assist statistics as kassist=kill+0.5*assist. Defaults to True.
        paint (bool, optional): Use paint stat to plot it as a bar behind the main stats. Defaults to True.
        kRange (tuple, optional): y-range for the kill+death ratios. Defaults to (0, 50).
        pRange (tuple, optional): y-range for the paint statistic. Defaults to (0, 2000).
        rScale (str, optional): Way the circular axis will be scaled. Defaults to 'symlog'.
        innerOffset (float, optional): Radius of the innermost circle to create a clear area at the centar of the plot. Defaults to 0.75.
        clockwise (bool, optional): Sorting of the battles starts at 12 o'clock and goes clockwise. Defaults to True.
        colorsTop (tuple, optional): Color of the line if kills are larger than deaths, and if they are not. Defaults to (cst.CLR_STATS['kill'], cst.CLR_STATS['death']).
        colorBars (color, optional): Color of the bars assigned to the paint statistic. Defaults to cst.CLR_PAINT.
        innerText (bool, optional): Add the inner label as the ratio of kills or kassists to deaths. Defaults to True.
        innerTextFmt (str, optional): Formatting string for the inner label. Defaults to '{:.2f}'.
        fontSize (int, optional): Font size for the inner label. Defaults to 20.
        fontColor (str, optional): Font color for the inner label. Defaults to '#00000066'.
        innerGuides (tuple, optional): Start, stop, increment values for the innermost guides on the radial axis. Defaults to (0, 6, 1).
        innerGuidesColor (str, optional): Color for the innermost guides. Defaults to "#00000066".
        outerGuides (tuple, optional): Start stop, increment values for the outermost guides on the radial axis. Defaults to (0, 50, 10).
        outerGuidesColor (str, optional): Color for the outer guides. Defaults to "#00000088".
        frameColor (str, optional): Color for the outermost radial frame. Defaults to "#00000011".

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    # Get variables -----------------------------------------------------------
    (outer, inner) = (
        np.array(playerHistory['kill']), 
        np.array(playerHistory['death'])
    )
    if kassist:
        outer = outer + (.5 * np.array(playerHistory['assist']))
    bar = (np.array(playerHistory['paint']) if paint else None)
    if innerText:
        text = np.sum(outer)/np.sum(inner)
    # Generate plot -----------------------------------------------------------
    (fig, ax) = plotIris(
        figAx, outer, inner, barArray=bar,
        tbRange=kRange, bRange=pRange, rScale=rScale, innerOffset=innerOffset,
        clockwise=clockwise, colorsTop=colorsTop, colorBars=colorBars,
        innerText=innerTextFmt.format(text), 
        fontSize=fontSize, fontColor=fontColor,
        innerGuides=innerGuides, innerGuidesColor=innerGuidesColor,
        outerGuides=outerGuides, outerGuidesColor=outerGuidesColor,
        frameColor=frameColor
    )
    return (fig, ax)