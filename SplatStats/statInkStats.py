#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.feature_extraction import DictVectorizer


###############################################################################
# Stats
###############################################################################
def calculateDominanceMatrixWins(statInkBattles):
    # Get the weapons dictionaries for each team ------------------------------
    btls = statInkBattles
    (alpha, bravo) = (
        btls[[f'A{i}-weapon' for i in range(1, 5)]],
        btls[[f'B{i}-weapon' for i in range(1, 5)]]
    )
    winrs = list(btls['win'])
    # Vectorize (encode) the weapons used by each team in the battles ---------
    vct = DictVectorizer(sparse=False)
    wpnsDA = [dict(Counter(alpha.iloc[i])) for i in range(alpha.shape[0])]
    wpnsDB = [dict(Counter(bravo.iloc[i])) for i in range(bravo.shape[0])]
    (wpnsVA, wpnsVB) = (vct.fit_transform(wpnsDA), vct.fit_transform(wpnsDA))
    wpnsNames = list(vct.get_feature_names_out())
    # Assemble matrix ---------------------------------------------------------
    domMtx = np.zeros((len(wpnsNames), len(wpnsNames)))
    for ix in range(len(winrs)):
        (bAWpns, bBWpns, winTeam) = (wpnsDA[ix], wpnsDB[ix], winrs[ix])
        (bAVctr, bBVctr) = (wpnsVA[ix], wpnsVB[ix])
        if winTeam:
            rxs = [wpnsNames.index(wpn) for wpn in bBWpns]
            for rx in rxs:
                domMtx[rx] = domMtx[rx]+bAVctr
        else:
            rxs = [wpnsNames.index(wpn) for wpn in bAWpns]
            for rx in rxs:
                domMtx[rx] = domMtx[rx]+bBVctr
    # Transpose and return ----------------------------------------------------
    domMtx = domMtx.T  
    return (wpnsNames, domMtx)



###############################################################################
# Plots
###############################################################################
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