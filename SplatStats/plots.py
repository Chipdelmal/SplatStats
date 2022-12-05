
import squarify
import numpy as np
import seaborn as sns
from pywaffle import Waffle
import matplotlib.pyplot as plt
from math import radians, log10
from matplotlib.patches import Rectangle
import SplatStats.constants as cst
import SplatStats.stats as stats
import SplatStats.auxiliary as aux
import SplatStats.colors as clr
import SplatStats.plotsAux as paux
import matplotlib
matplotlib.rcParams['font.family'] = ['monospace']
# matplotlib.rcParams['font.stretch'] = ['condensed']
import warnings
warnings.filterwarnings("ignore")


def plotKillsAndDeathsHistogram(
        figAx, playerHistory, killRange, 
        binSize=1, assistsAdjustment=True, normalized=True,
        yRange=(-.25, .25), aspect=.25, alpha=.75, edgecolor='#000000',
        kColor=cst.CLR_STATS['kill'], dColor=cst.CLR_STATS['death'],
        labelsDict={'fontsize': 10},
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
    xLab = (
        'Kills/Deaths' 
        if not assistsAdjustment else 
        '(Kills+1/2*Assists)/Deaths'
    )
    ax.set_xlabel(xLab, fontdict=labelsDict)
    ax.set_ylabel('Frequency', fontdict=labelsDict)
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
    mStr = f''' Matches: {mNum:06d}
 Paint: {paint:08d} (avg: {pAvg:.0f} & per min: {ppm:.0f})
 Kills: {kNum:08d} (avg: {kAvg:.3f} & per min: {kpm:.3f})
 Deaths: {dNum:08d} (avg: {dAvg:.3f} & per min: {dpm:.3f})
 Assists: {aNum:08d} (avg: {aAvg:.3f} & per min: {apm:.3f})
 KAssists: {int(kaNum):06d} (avg: {kaAvg:.3f} & per min: {kapm:.3f})
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
        pad=0.1, lw=2, ec='#00000055', alpha=.65
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
        pad=0.1, lw=2, ec='#00000055', alpha=.65,
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
        tbRange=(0, 50), bRange=(0, 2000), lw=0.35, alpha=.75,
        rScale='symlog', innerOffset=0.75, clockwise=True,
        colorsTop=(cst.CLR_STATS['kill'], cst.CLR_STATS['death']),
        colorBars=cst.CLR_PAINT,
        innerText=None, fontSize=20, fontColor='#000000CC',
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
        lw=lw, colors=colors, alpha=alpha
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
    ax.yaxis.grid(True, color=outerGuidesColor, ls='-', lw=0.2, zorder=-10)
    ax.spines["start"].set_color("none")
    ax.spines["polar"].set_color(frameColor)
    # Return figure -----------------------------------------------------------
    return (fig, ax)


def plotkillDeathIris(
        figAx, playerHistory, kassist=True, paint=True,
        kRange=(0, 50), pRange=(0, 2000), alpha=.85,
        rScale='symlog', innerOffset=0.75, clockwise=True,
        colorsTop=(cst.CLR_STATS['kill'], cst.CLR_STATS['death']),
        colorBars=cst.CLR_PAINT,
        innerText=True, innerTextFmt='{:.2f}',
        fontSize=20, fontColor='#00000066',
        innerGuides=(0, 10, 1), innerGuidesColor="#00000066",
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
        figAx, outer, inner, barArray=bar, alpha=alpha,
        tbRange=kRange, bRange=pRange, rScale=rScale, innerOffset=innerOffset,
        clockwise=clockwise, colorsTop=colorsTop, colorBars=colorBars,
        innerText=innerTextFmt.format(text), 
        fontSize=fontSize, fontColor=fontColor,
        innerGuides=innerGuides, innerGuidesColor=innerGuidesColor,
        outerGuides=outerGuides, outerGuidesColor=outerGuidesColor,
        frameColor=frameColor
    )
    return (fig, ax)


def plotAwardFrequencies(
        figAx, awardFrequencies,
        alpha=0.4, color=cst.CLR_BAR, textSize=8, **kwargs
    ):
    """Plots player's award frequencies as a barchart.

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        awardFrequencies (tuples): Award frequency tuples from getAwardFrequencies function.
        alpha (float, optional): Alpha value for the chart. Defaults to 0.4.
        color (hexString, optional): Color for the bars. Defaults to cst.CLR_BAR.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    (labels, values) = (
        [i[0] for i in awardFrequencies], [i[1] for i in awardFrequencies]
    )
    yPos = np.arange(len(labels), 0, -1)
    # Generate figure ---------------------------------------------------------
    (fig, ax) = figAx
    ax.barh(
        yPos, values, 
        align='center', alpha=alpha, color=color,
        **kwargs        
    )
    ax.set_yticks(yPos, labels, fontsize=textSize)
    return (fig, ax)


def plotMatchTypeBars(
        stagesByTypeFlat, metric, aggMetrics=('win', 'total matches'),
        yRange=(0, 1), cDict=cst.CLR_STAGE, alpha=0.75,
        wspace=0.05, hspace=0, aspect=1, fontsize=8,
        sorting=[
            'Turf War', 'Tower Control', 'Rainmaker', 
            'Splat Zones', 'Clam Blitz', 'Tricolor Turf War'
        ],
        percentLegend={'color': '#00000020', 'fontsize': 50},
        countsLegend={'color': '#00000044', 'fontsize': 8},
        digs=3,
        percentage=True,
        textOffset=0.01,
        fmt='{:.2f}'
    ):
    """Generates a grid of seaborn plots with stats broken down by match type and stage.

    Args:
        stagesByTypeFlat (dataframe): Dataframe obtained by running ammendStagesStatsByType on the calcStagesStatsByType structure.
        metric (str): Main metric for bar sizes.
        aggMetrics (tuple of strings): These two metrics are used to calculate a fraction of metric1/metric2 on the aggregate value displayed. Defaults to ('win', 'total matches').
        yRange (tuple, optional): y-axis plot range. Defaults to (0, 1).
        cDict (dict, optional): Colors dictionary in the form {'stage name': hexColor}. Defaults to cst.CLR_STAGE.
        alpha (float, optional): Alpha value for bars. Defaults to 0.75.
        wspace (float, optional): Frames horizontal spacing. Defaults to 0.05.
        hspace (int, optional): Frames vertical spacing. Defaults to 0.
        aspect (int, optional): Boxes aspect ratio. Defaults to 1.
        fontsize (int, optional): Labels font size. Defaults to 8.
        sorting (list, optional): Sorting of the match-types. Defaults to [ 'Turf War', 'Tower Control', 'Rainmaker', 'Splat Zones', 'Clam Blitz' ].
        percentLegend (dict, optional): Style for the main aggregate label. Defaults to {'color': '#00000020', 'fontsize': 50}.
        countsLegend (dict, optional): Style for the counts labels on the bars. Defaults to {'color': '#00000044', 'fontsize': 8}.
        digs (int, optional): Digits for zfill. Defaults to 3.
        percentage (bool, optional): Plot fractions as percentages? Defaults to True.
        fmt (str, optional): Format string for plot aggregate's value. Defaults to '{:.2f}'.

    Returns:
        sns facetgrid: Seaborn facetgrid object.
    """    
    allStages = sorted(stagesByTypeFlat['stage'].unique())
    g = sns.FacetGrid(
        stagesByTypeFlat, col="match type", aspect=.75,
        col_order=sorting
    )
    g.map(
        sns.barplot, 'stage', metric, 
        palette=[cDict[k] for k in allStages], 
        alpha=alpha, order=allStages
    )
    g.figure.subplots_adjust(wspace=wspace, hspace=hspace)
    # g.set_xticklabels(allStages, rotation=90)
    g.set_axis_labels('', metric)
    g.set_titles('{col_name}')
    # Modify axes -------------------------------------------------------------
    for ax in g.axes.flatten():
        for _, spine in ax.spines.items():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(1)
        ax.set_box_aspect(aspect)
        ax.set_ylim(*yRange)
        ax.set_xticklabels(allStages, fontdict={'fontsize': fontsize})
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_yticklabels(
            [f'{i:.1f}' for i in ax.get_yticks()], 
            fontdict={'fontsize': fontsize}
        )
        mType = ax.get_title()
        fltr = (stagesByTypeFlat['match type'] == mType)
        dataMatchType = stagesByTypeFlat[fltr]
        tmatch = sum(dataMatchType[aggMetrics[1]])
        if (tmatch > 0):
            ratio = sum(dataMatchType[aggMetrics[0]])/tmatch
        else:
            ratio = 0
        if percentage:
            ax.text(
                0.525, 0.5, 
                '{}%'.format(round(ratio*100)), 
                ha='center', va='center',
                transform=ax.transAxes,
                **percentLegend
            )
        else:
            ax.text(
                0.525, 0.5, 
                fmt.format(ratio), 
                ha='center', va='center',
                transform=ax.transAxes,
                **percentLegend
            )
        # Matches counts -------------------------------------------------------
        x_min, x_max = ax.get_xlim()
        ticks = [(tick - x_min)/(x_max - x_min) for tick in ax.get_xticks()]
        for (ix, st) in enumerate(allStages):
            fltrStage = (dataMatchType['stage'] == st)
            stageData = dataMatchType[fltrStage]
            if stageData.shape[0] > 0:
                ax.text(
                    ticks[ix]+textOffset, .03, 
                    '{}'.format(
                        str(int(stageData[aggMetrics[1]])).zfill(digs)
                    ), 
                    ha='center', va='bottom',
                    rotation=90,
                    transform=ax.transAxes,
                    **countsLegend
                )
            else:
                ax.text(
                    ticks[ix], .03, 
                    '{}'.format(
                        str(0).zfill(digs)
                    ), 
                    ha='center', va='bottom',
                    rotation=90,
                    transform=ax.transAxes,
                    **countsLegend
                )
        ax.text(
            0.975, 0.975, 
            '{}'.format(
                str(sum(dataMatchType[aggMetrics[1]])).zfill(digs)
            ), 
            ha='right', va='top', transform=ax.transAxes,
            **countsLegend
        )
    return g


def plotRanking(
        figAx,
        rankingDF, 
        normalized=True, yLim=None, xLim=None,
        colors=['#C70864', '#C920B7', '#4B25C9', '#830B9C', '#2CB721'],
        categories=['kill', 'death', 'assist', 'paint', 'special'],
        widthBar=0.9, title=True, pad=0, titlePos=(0.975, .85),
        fontsize=20,
        **kwargs
    ):
    """Generates barcharts on stats for player's ranking across categories.

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        rankingDF (dataframe): Either getPlayerAlliedRanking or getPlayerFullRanking dataframe on battle data.
        normalized (bool, optional): If true, data is scaled to proportions (0 to 1) instead of raw frequencies. Defaults to True.
        xLim (tuple, optional): Plot limits on x axis Defaults to None.
        yLim (tuple, optional): Plot limits on y axis. Defaults to None.
        colors (list, optional): Color palette for bars. Defaults to ['#C70864', '#C920B7', '#4B25C9', '#830B9C', '#2CB721'].
        categories (list, optional): Categories for the ranks (in order). Defaults to ['kill', 'death', 'assist', 'paint', 'special'].
        widthBar (float, optional): Bars width. Defaults to 0.9.
        title (bool, optional): If true, the title of the plot is printed. Defaults to True.
        titlePos (tuple, optional): Position for plots' title. Defaults to (0.975, .9).
        pad (int, optional): Padding for plots along the grid. Defaults to 0.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    (fig, axes) = figAx
    fig.tight_layout(pad=pad)
    for (col, ax, cat) in zip(colors, axes, categories):
        rankingDF[cat].value_counts(normalize=normalized).sort_index().plot(
            ax=ax, kind='bar', color=col, width=widthBar,
            **kwargs
        )
        if title:
            ax.text(
                titlePos[0], titlePos[1], cat, 
                transform=ax.transAxes, ha="right", fontsize=fontsize*.75
            )
        if yLim:
            ax.set_ylim(*yLim)
        if xLim:
            ax.set_xlim(*xLim)
    axes[-1].set_xticklabels([i+1 for i in axes[-1].get_xticks()], rotation=0)
    axes[-1].set_xlabel("Rank", fontsize=fontsize)
    axes[-1].set_ylabel("Frequency", fontsize=fontsize)
    return (fig, axes)


def plotWaffleStat(
        figAx, playerHistory,
        function=sum, grouping='main weapon', stat='kill',
        rows=50, columns=50, startingLocation='NW', blockArranging='snake',
        intervalRatioX=0.5, intervalRatioY=0.5,
        colors=clr.ALL_COLORS, alpha=.6,
        fmt="{:.2f}",
        title=True,
        vertical=True,
        legendDict={
            'loc': 'upper left',
            'bbox_to_anchor': (1, 1),
            'ncol': 1,
            'framealpha': 0,
            'fontsize': 10
        },
        **kwargs
    ):
    """Generates a waffle plot of aggregated statistics on player's history (eg. sums of kills broken by main weapon).

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        playerHistory (dataframe): Player history dataframe.
        function (function, optional): Aggregation function for groupby. Defaults to sum.
        grouping (str, optional): Category over which the aggregation will be done. Defaults to 'main weapon'.
        stat (str, optional): Statistic to use in the plot. Defaults to 'kill'.
        rows (int, optional): Number of rows for waffle. Defaults to 50.
        columns (int, optional): Number of columns for waffle. Defaults to 50.
        startingLocation (str, optional): Waffle's starting locations (see pywaffle's docs). Defaults to 'NW'.
        blockArranging (str, optional): Block arranging (see pywaffle's docs). Defaults to 'snake'.
        intervalRatioX (float, optional): Spacing over x axis. Defaults to 0.5.
        intervalRatioY (float, optional): Spacing over y axis. Defaults to 0.5.
        colors (list, optional): List of hex colors. Defaults to clr.ALL_COLORS.
        alpha (float, optional): Alpha for the colors. Defaults to .6.
        fmt (str, optional): Formating for the title number. Defaults to "{:.2f}".
        title (bool, optional): Prints title if true. Defaults to True.
        legendDict (dict, optional): Dictionary for labels (see pywaffle's docs). Defaults to { 'loc': 'upper left', 'bbox_to_anchor': (1, 1), 'ncol': 1, 'framealpha': 0, 'fontsize': 10 }.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """    
    (fig, ax) = figAx
    # Aggregate ---------------------------------------------------------------
    df = playerHistory.groupby(grouping).agg(function)
    cols = [
        i+aux.alphaToHex(alpha) for i in colors[:len(df.index)]
    ]
    # Waffle ------------------------------------------------------------------
    Waffle.make_waffle(
        ax=ax,
        rows=rows, 
        columns=columns,
        values=df[stat],
        starting_location=startingLocation,
        vertical=vertical,
        block_arranging_style=blockArranging,
        colors=cols,
        interval_ratio_x=intervalRatioX,
        interval_ratio_y=intervalRatioY,
        labels=[
            f"{k} ({float(v/sum(df[stat])*100):.2f}%)" 
            for (k, v) in zip(df.index, df[stat])
        ],
        legend=legendDict,
        **kwargs
    )
    if title:
        plt.title(f"{stat} ("+fmt.format(function(df[stat]))+")")
    return (fig, ax)


def plotCircularBarchartStat(
        playerHistory, figAx=None,
        cat='main weapon', stat='kill', aggFun=np.sum,
        logScale=False, ticksStep=10,
        rRange=(0, 270), yRange=None,
        labels=True, labelQty=False, colors=clr.ALL_COLORS,
        origin='N', direction=1,
        ticksFmt={
            'lw': 1, 'range': (-0.5, -0.25), 
            'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.2f}'
        },
        labelFmt={
            'color': '#000000EE', 'fontsize': 10, 
            'ha': 'left', 'fmt': '{:.1f}'
        }
    ):
    """Generates a radial barchart for 

    Args:
        figAx (tuple): (fig, ax) tuple as initialized by matplotlib (plt.subplots).
        playerHistory (dataframe): Player history dataframe.
        cat (str): Category over which the aggregation will be done. Defaults to 'main weapon'.
        stat (str): Statistic to use in the plot. Defaults to 'kill'.
        aggFun (function, optional): Aggregation function for groupby. Defaults to np.sum.
        autoRange (bool, optional): Auto-scales the radial plot with data min and data max. Defaults to True.
        logScale (bool, optional): Uses log-scale for the radial bars. Defaults to True.
        gStep (int, optional): Number of equally-spaced steps for radial ticks. Defaults to 30.
        rRange (tuple, optional): Radial angles for the plot. Defaults to (0, 270).
        xRange (tuple, optional): Values to map onto the rRange values. Defaults to (0, 10).
        colors (_type_, optional): List of hex colors for bars. Defaults to clr.ALL_COLORS.

    Returns:
        (fix, ax): Matplotlib's fig and ax objects.
    """
    # Gather data -------------------------------------------------------------
    df = playerHistory.groupby(cat).agg(aggFun)
    df.sort_values(by=[stat], inplace=True)
    catVals = list(df[stat])
    # Generate chart ----------------------------------------------------------
    (fig, ax) = polarBarChart(
        xVals=list(df.index), yVals=catVals,
        figAx=figAx, logScale=logScale, ticksStep=ticksStep,
        rRange=rRange, yRange=yRange, colors=colors, labels=labels,
        origin=origin, direction=direction, labelQty=labelQty, 
        ticksFmt=ticksFmt, labelFmt=labelFmt
    )
    return (fig, ax)


def polarBarChart(
        xVals, yVals,
        figAx=None,
        logScale=False, ticksStep=10,
        rRange=(0, 270), yRange=None,
        colors=clr.ALL_COLORS,
        labels=True, labelQty=False,
        origin='N', direction=1,
        ticksFmt={
            'lw': 1, 'range': (-0.5, -0.25), 
            'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.1f}'
        },
        labelFmt={
            'color': '#000000EE', 'fontsize': 10, 
            'ha': 'left', 'fmt': '{:.1f}'
        }
    ):
    # Generate (fig, ax) if needed --------------------------------------------
    if figAx is None:
        (fig, ax) = plt.subplots(
            figsize=(8, 8), subplot_kw={"projection": "polar"}
        )
    else:
        (fig, ax) = figAx
    # Get value ranges --------------------------------------------------------
    (minValY, maxValY) = [
        0 if not yRange else yRange[0],
        max(yVals) if not yRange else yRange[1]
    ]
    if not yRange:
        yRange = (minValY, maxValY)
    # Define grid -------------------------------------------------------------
    stepSizeY = maxValY/ticksStep
    gridY = np.arange(minValY, maxValY+maxValY/stepSizeY, stepSizeY)
    # Log-scale if needed -----------------------------------------------------
    if logScale:
        (gridYSca, yValsSca, yRangeSca) =  [
            [log10(i+1) for i in j] for j in (gridY, yVals, yRange)
        ]
    else:
        (gridYSca, yValsSca, yRangeSca) =  (gridY, yVals, yRange)
    # Convert heights into radii ----------------------------------------------
    (angleHeights, grids) = [
        [np.interp(i, yRangeSca, rRange) for i in j] 
        for j in (yValsSca, gridYSca)
    ]
    # Generate Plot -----------------------------------------------------------
    for (i, ang) in enumerate(angleHeights):
        ax.barh(i, radians(ang), color=colors[i])
    # Gridlines and axes ------------------------------------------------------
    ax.vlines(
        [radians(i) for i in grids[:ticksStep+1]], 
        len(xVals)+ticksFmt['range'][0], len(xVals)+ticksFmt['range'][1],
        colors=ticksFmt['color']
    )
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_ylim(-.5, len(yVals)-0.1)
    ax.spines['polar'].set_visible(False)
    ax.set_theta_zero_location(origin)
    ax.set_theta_direction(direction)
    ax.set_rlabel_position(0)
    # Labels ------------------------------------------------------------------
    labelsText = [ticksFmt['fmt'].format(i) for i in gridY] if labels else []
    ax.set_thetagrids(
        grids[:ticksStep+1], labelsText[:ticksStep+1], 
        color=ticksFmt['color']
    )
    # Categories Markers ------------------------------------------------------
    if labelQty:
        labelText = [
            f' {w} ('+labelFmt['fmt'].format(v)+')' for (w, v) in zip(xVals, yVals)
        ]
    else:
        labelText = [f' {i}' for i in xVals]
    ax.set_rgrids(
        [i for i in range(len(xVals))], 
        labels=labelText,
        va='center', **labelFmt
    )
    # Return results ----------------------------------------------------------
    return (fig, ax)