#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import SplatStats.colors as clr
import SplatStats.plots as pts


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
        scaler=1e3,
        colors=[
            '#2E0CB5', '#B400FF', '#6BFF00', '#525CF5', '#FDFF00', '#D01D79'
        ]
    ):
    (series, data) = (
        list(lbyFreq.keys()), [[int(i)] for i in list(lbyFreq.values())]
    )
    data = [[i[0]/scaler] for i in data]
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
        value_format="{:.0f}k",
        fontsize=8.5, xTickOffset=0.7
    )
    ax.axis('off')
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.text(
        -2.25, 0.5, 'Total matches: {:.0f}k'.format(np.sum(data)),
        fontsize=20,
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes,
        rotation=90
    )
    return (fig, ax)


def plotDominanceMatrix(
        matrix, 
        figAx=None, range=(-1, 1), 
        cmap=clr.colorPaletteFromHexList(['#D01D79', '#FFFFFF', '#1D07AC'])
    ):
    if not figAx:
        (fig, ax) = plt.subplots(figsize=(20, 20))
    else:
        (fig, ax) = figAx
    im = ax.matshow(matrix, vmin=range[0], vmax=range[1], cmap=cmap)
    ax.set_xticks(np.arange(0, len(matrix.shape[0])))
    ax.set_yticks(np.arange(0, len(matrix.shape[0])))
    # ax.set_xticklabels(tLabs, rotation=90, fontsize=12.5)
    # ax.set_yticklabels(lLabs, fontsize=12.5)
    return (fig, ax)