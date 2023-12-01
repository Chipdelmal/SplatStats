#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import SplatStats.colors as clr
import SplatStats.plots as pts
import SplatStats.statInkConstants as cst


def plotStackedBar(
        data, series_labels, labels=None, figAx=None, category_labels=None, 
        show_values=False, value_format="{}", y_label=None, 
        colors=None, textColor='#000000', fontsize=12,
        xTickOffset=5
    ):
    if not figAx:
        (fig, ax) = plt.figure(figsize=(2, 20))
    else:
        (fig, ax) = figAx

    ny = len(data[0])
    ind = list(range(ny))
    axes = []
    (cum_size, data) = (np.zeros(ny), np.array(data))

    for i, row_data in enumerate(data):
        color = colors[i] if colors is not None else None
        axes.append(plt.bar(
            ind, row_data, bottom=cum_size, 
            label=series_labels[i], color=color
        ))
        cum_size += row_data

    if category_labels:
        ax.xticks(ind, category_labels)

    if show_values:
        for (ix, axis) in enumerate(axes):
            for (_, bar) in enumerate(axis):
                w, h = bar.get_width(), bar.get_height()
                if not labels:
                    ax.text(
                        bar.get_x()+w/2, bar.get_y()+h/2, 
                        value_format.format(h), 
                        ha="center", va="center", 
                        color=textColor, fontsize=fontsize
                    )
                else:
                    ax.text(
                        bar.get_x()-xTickOffset,# +w/2, 
                        bar.get_y()+h/2, 
                        '{}\n{}'.format(labels[ix], value_format.format(h)), 
                        ha="center", va="center",
                        color=textColor, fontsize=fontsize
                    )
    ax.set_xlim(-w/2, w/2)
    ax.set_ylim(0, np.sum(data))
    return (fig, ax)


def barChartLobby(
        lbyFreq,
        figAx=None,
        scaler=('k', 1e3),
        fontSizes=(8.5, 20),
        colors=[
            '#2E0CB5', '#B400FF', '#6BFF00', 
            '#525CF5', '#FDFF00', '#D01D79', 
            '#E2E2E2'
        ]
    ):
    (series, data) = (
        list(lbyFreq.keys()), [[int(i)] for i in list(lbyFreq.values())]
    )
    data = [[i[0]/scaler[1]] for i in data]
    if figAx:
        (fig, ax) = figAx
    else:
        (fig, ax) = plt.subplots(figsize=(0.4, 20))
    (fig, ax) = plotStackedBar(
        data, series, 
        labels=[i.replace(' ', '\n') for i in list(lbyFreq.keys())],
        figAx=(fig, ax),
        category_labels=False, 
        show_values=True, 
        colors=colors,
        value_format="{:.0f}"+scaler[0],
        fontsize=fontSizes[0], xTickOffset=0.7
    )
    ax.axis('off')
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.text(
        -2.25, 0.5, 'Total matches: {:.0f}{}'.format(np.sum(data), scaler[0]),
        fontsize=fontSizes[1],
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes,
        rotation=90
    )
    return (fig, ax)


def plotDominanceMatrix(
        sNames, sMatrix, sSort, mMatrix,
        figAx=None, vRange=(-1, 1), scaler=('k', 1e3),
        cmap=clr.colorPaletteFromHexList(['#D01D79', '#FFFFFF', '#1D07AC']),
        fontSize=10
    ):
    counts = [np.sum(r>0) for r in sMatrix]
    (mWpnWins, mWpnLoss) = (
        np.sum(mMatrix, axis=1)/4, 
        np.sum(mMatrix, axis=0)/4
    )
    tVect = (mWpnWins+mWpnLoss)[sSort]
    lLabs = [
        '{} ({})'.format(n, c) 
        for (n, c) in zip(sNames, counts)
    ]
    tLabs = [
        '({}{}) {}'.format(c, scaler[0], n)
        for (n, c) in zip(sNames, [int(i) for i in tVect/scaler[1]])
    ]
    # Generating matrix ------------------------------------------------------
    if not figAx:
        (fig, ax) = plt.subplots(figsize=(20, 20))
    else:
        (fig, ax) = figAx
    ax.matshow(sMatrix, vmin=vRange[0], vmax=vRange[1], cmap=cmap)
    ax.set_xticks(np.arange(0, len(sNames)))
    ax.set_yticks(np.arange(0, len(sNames)))
    ax.set_xticklabels(tLabs, rotation=90, fontsize=fontSize)
    ax.set_yticklabels(lLabs, fontsize=fontSize)
    return (fig, ax)


def plotPolarFrequencies(
        wpnFreq, wpnRank, 
        figAx=None, topRank=None,
        yRange=(0, 3e5), rRange=(0, 180), 
        edge={'lw': 0, 'lc': '#000000'},
        fontSizes=(1, 3.75), fontColors=('#000000', '#000000'),
        ticksStep=4, 
        direction=1,
        colors=clr.ALL_COLORS,
        logScale=False
    ):
    # Generate figAx if needed ------------------------------------------------
    if not figAx:
        (fig, ax) = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})
    else:
        (fig, ax) = figAx
    # Get labels and freqs ----------------------------------------------------
    labels = [
        '{:02d}. {} ({}%)'.format(ix, n, int(f*100)) for (ix, n, f) in wpnRank
    ]
    (labs, freqs) = (
        labels[::-1], 
        list(wpnFreq.values())[::-1]
    )
    # Get top if needed -------------------------------------------------------
    if topRank:
        (labs, freqs) = (
            labs[topRank[0]:topRank[1]], 
            freqs[topRank[0]:topRank[1]]
        )
    # Generate plot -----------------------------------------------------------
    (fig, ax) = pts.polarBarChart(
        labs, freqs,
        logScale=logScale,
        direction=direction, ticksStep=ticksStep,
        yRange=yRange, rRange=rRange, 
        colors=[c+'DD' for c in colors],
        edgecolor=edge['lc'], linewidth=edge['lw'],
        figAx=(fig, ax),
        ticksFmt={
            'lw': 1, 'range': (-.2, 1), 
            'color': fontColors[0], 'fontsize': fontSizes[0], 'fmt': '{:.1e}'
        },
        labelFmt={
            'color': fontColors[1], 'fontsize': fontSizes[1], 
            'ha': 'left', 'fmt': '{:.1f}'
        }
    )
    xlabels = ax.get_xticklabels()
    for txt in xlabels:
        lab = txt.get_text()
        txt.set_text('{:.0f}k'.format(float(lab)/1e3))
    ax.set_xticklabels(xlabels, rotation=0, fontsize=fontSizes[0])
    return (fig, ax)


def plotGaussianLobby(
        lbyDaily, lbyGaussDaily,
        figAx=None, ylim=(0, -1250), xticksDelta=30,
        gModesColors = ['#DE0B64FF', '#FDFF00FF', '#0D37C3FF', '#71DA0CFF', '#531BBAFF']
    ):
    gModes = list(lbyDaily.columns)
    if not figAx:
        (fig, ax) = (plt.figure(figsize=(20, 3)), plt.axes())
    else:
        (fig, ax) = figAx
    ax.stackplot(
        lbyGaussDaily[0][0], *[-y[1] for y in lbyGaussDaily], 
        labels=gModes, baseline='zero',
        colors=gModesColors
    )
    ax.legend(loc='upper left').remove()
    ax.set_xlim(0, lbyGaussDaily[0][0][-1])
    ax.set_ylim(ylim[0], ylim[1])
    xtickRan = np.arange(0, lbyGaussDaily[0][0][-1], xticksDelta)
    # ax.set_ylim(ax.get_ylim()[::-1])
    ax.xaxis.tick_top()
    ax.set_xticks(
        xtickRan, 
        [
            '{}/{}/{}'.format(
                lbyDaily.index[int(i)].day,
                lbyDaily.index[int(i)].month, 
                lbyDaily.index[int(i)].year
            )
            for i in xtickRan
        ],
        ha='left', va='bottom', rotation=0, fontsize=8
    )
    ax.set_yticks([], [])
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return (fig, ax)


def plotWeaponsStrips(
        weaponsHists, weaponsList, stat,
        figAx=None,
        weaponsSummary=None,
        color='#1A1AAEDD', range=(0, 50),
        cScaler=(lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 1])),
        binSize=1,
        edgecolor='#000000dd',
        statcolor='#000000ff'
    ):
    wpnList = weaponsList[::-1]
    bCol = mcolors.ColorConverter().to_rgba(color)
    if figAx:
        (fig, ax) = figAx
    else:
        (fig, ax) = plt.subplots(figsize=(5, 20))
    for (ix, wpn) in enumerate(wpnList):
        wpnData = weaponsHists[wpn][stat]
        for (x, k) in enumerate(wpnData):
            alpha = cScaler(k)
            ax.add_patch(
                Rectangle(
                    (x, ix), binSize, 1,
                    facecolor=(bCol[0], bCol[1], bCol[2], alpha),
                    edgecolor=edgecolor,
                )
            )
    if weaponsSummary:
        for (ix, wpn) in enumerate(wpnList):
            wpnData = weaponsSummary[wpn][stat] + binSize/2
            ax.vlines(
                wpnData, ix+0.25, ix+0.75,
                colors=statcolor,
                lw=2.5, ls='-'
            )
    ax.set_ylim(0, len(wpnList))
    ax.set_yticks(np.arange(0.5, len(wpnList), 1))
    ax.set_yticklabels(wpnList)
    ax.set_xlim(range[0], range[1]+binSize)
    # ax.xaxis.tick_top()
    ax.set_xticks(np.arange(range[0]+binSize/2, range[1]+binSize/2+1/2, 5))
    ax.set_xticklabels(np.arange(range[0], range[1]+1, 5))
    ax.set_title('{}'.format(stat), fontdict={'fontsize': 20})
    return (fig, ax)



def plotWeaponStrip(
        weaponsHists, weaponName, wpnStats,
        figAx=None,
        weaponsSummary=None,
        styleDictionary=cst.INKSTATS_STYLE,
        binSize=1,
        edgecolor='#000000',
        statcolor='#000000'
    ):
    ranges = np.array([styleDictionary[c]['range'] for c in wpnStats]).T
    range = (min(ranges[0]), max(ranges[1]))
    bCols = [
        mcolors.ColorConverter().to_rgba(styleDictionary[c]['color']) 
        for c in wpnStats
    ]
    cScalers = [styleDictionary[c]['scaler'] for c in wpnStats]
    if figAx:
        (fig, ax) = figAx
    else:
        (fig, ax) = plt.subplots(figsize=(20, 2))
    wpnFullData = weaponsHists[weaponName]
    for (ix, stat) in enumerate(wpnStats):
        wpnData = wpnFullData[stat]
        for (x, k) in enumerate(wpnData):
            alpha = cScalers[ix](k)
            bCol = bCols[ix]
            ax.add_patch(
                Rectangle(
                    (x, ix), binSize, 1,
                    facecolor=(bCol[0], bCol[1], bCol[2], alpha),
                    edgecolor=edgecolor,
                )
            )
    if weaponsSummary:
        wpnFullSummary = weaponsSummary[weaponName]
        for (ix, sta) in enumerate(wpnStats):
            wpnData = wpnFullSummary[sta] + binSize/2
            ax.vlines(
                wpnData, ix+0.25, ix+0.75,
                colors=statcolor,
                lw=2.5, ls='-'
            )
    ax.set_xticks(np.arange(range[0]+binSize/2, range[1]+binSize/2+1/2, 5))
    ax.set_xticklabels(np.arange(range[0], range[1]+1, 5))
    ax.set_xlim(range[0], range[1]+binSize)
    ax.set_ylim(0, len(wpnStats))
    ax.set_yticks(np.arange(0.5, len(wpnStats), 1))
    ax.set_yticklabels(wpnStats)
    ax.set_title('{}'.format(weaponName), fontdict={'fontsize': 20})
    return (fig, ax)