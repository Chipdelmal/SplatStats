#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
from sklearn.feature_extraction import DictVectorizer

###############################################################################
# Stats
###############################################################################
def calculateDominanceMatrixWins(btls, wpnsNames=None):
    btlsNum = btls.shape[0]
    # Get weapons used by each team, and who won ------------------------------
    winAlpha = list(btls['win'])
    tmsWpns = getTeamsWeapons(btls)
    (alpha, bravo) = (tmsWpns['alpha'], tmsWpns['bravo'])
    # Get all the weapons used if needed --------------------------------------
    wNames = (getWeaponsSet(btls) if not wpnsNames else wpnsNames)
    wpnsNumbr = len(wNames)
    # Generate matrix ---------------------------------------------------------
    domMtx = np.zeros((wpnsNumbr, wpnsNumbr))
    bix = 0
    for bix in range(btlsNum):
        # Get names for weapons in both teams ---------------------------------
        (wpnsNmA, wpnsNmB) = (list(alpha.iloc[bix]), list(bravo.iloc[bix]))
        # Get indices for weapons in both teams -------------------------------
        (wpnsIxA, wpnsIxB) = (
            [wNames.index(w) for w in wpnsNmA],
            [wNames.index(w) for w in wpnsNmB]
        )
        if winAlpha[bix]:
            # Team Alpha won --------------------------------------------------
            for ixA in wpnsIxA:
                for ixB in wpnsIxB:
                    domMtx[ixA, ixB] = domMtx[ixA, ixB] + 1
        else:
            # Team Bravo won --------------------------------------------------
            for ixB in wpnsIxB:
                for ixA in wpnsIxA:
                    domMtx[ixB, ixA] = domMtx[ixB, ixA] + 1
    return (wNames, domMtx)


def getTeamsWeapons(btls):
    ran = (1, 5)
    (alpha, bravo) = (
        btls[[f'A{i}-weapon' for i in range(*ran)]],
        btls[[f'B{i}-weapon' for i in range(*ran)]]
    )
    return {'alpha': alpha, 'bravo': bravo}


def getWeaponsFrequencies(btls):
    tmsWpns = getTeamsWeapons(btls)
    wpns = flatten([list(tmsWpns[t].stack()) for t in ('alpha', 'bravo')])
    wpnsCount = OrderedDict(Counter(wpns).most_common())
    return wpnsCount


def getLobbyFrequencies(btls):
    cntr = Counter(btls['lobby'])
    lobby = OrderedDict(Counter(cntr).most_common())
    return lobby


def getModeFrequencies(btls):
    cntr = Counter(btls['mode'])
    gmode = OrderedDict(Counter(cntr).most_common())
    return gmode


def getWeaponsSet(btls):
    tmsWpns = getTeamsWeapons(btls)
    (alpha, bravo) = (tmsWpns['alpha'], tmsWpns['bravo'])
    wpnsSet = (set(alpha.stack()) | set(bravo.stack()))
    wpnsNames = sorted(list(wpnsSet))
    return wpnsNames


def flatten(l):
    return [item for sublist in l for item in sublist]


def getWeaponsWLT(btls, wpnsNames=None):
    (tmsWps, alphaWin) = (getTeamsWeapons(btls), btls['win'])
    wNames = (getWeaponsSet(btls) if not wpnsNames else wpnsNames)
    # Iterate through battles -------------------------------------------------
    wpnWL = np.zeros((len(wNames), 3))
    for bix in range(btls.shape[0]):
        (tA, tB) = [list(tmsWps[a].iloc[bix]) for a in ('alpha', 'bravo')]
        if alphaWin.iloc[bix]:
            # Team A won ------------------------------------------------------
            (wix, lix) = ([wNames.index(w) for w in tA], [wNames.index(w) for w in tB])
        else:
            # Team B won ------------------------------------------------------
            (lix, wix) = ([wNames.index(w) for w in tA], [wNames.index(w) for w in tB])
        # Update weapons entries ----------------------------------------------
        for ix in range(4):
            # Add one to winning ----------------------------------------------
            wpnWL[wix[ix],0] = wpnWL[wix[ix],0]+1
            wpnWL[wix[ix],2] = wpnWL[wix[ix],2]+1
            # Add one to losing -----------------------------------------------
            wpnWL[lix[ix],1] = wpnWL[lix[ix],1]+1
            wpnWL[lix[ix],2] = wpnWL[lix[ix],2]+1
    return (wNames, wpnWL)


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


