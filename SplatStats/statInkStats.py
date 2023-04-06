#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import Counter, OrderedDict
import SplatStats.stats as stt


def calculateDominanceMatrix(btls, wpnsNames=None, dtype=np.uint32):
    btlsNum = btls.shape[0]
    # Get weapons used by each team, and who won ------------------------------
    winAlpha = list(btls['win'])
    tmsWpns = getTeamsWeapons(btls)
    (alpha, bravo) = (tmsWpns['alpha'], tmsWpns['bravo'])
    # Get all the weapons used if needed --------------------------------------
    wNames = (getWeaponsSet(btls) if not wpnsNames else wpnsNames)
    wpnsNumbr = len(wNames)
    # Generate matrix ---------------------------------------------------------
    domMtx = np.zeros((wpnsNumbr, wpnsNumbr), dtype=dtype)
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


def normalizeDominanceMatrix(
        wNames, domMtx, 
        sorted=True
    ):
    # Initialize matrix -------------------------------------------------------
    mSize = len(domMtx)
    tauW = np.zeros((mSize, mSize))
    # Iterate through rows ----------------------------------------------------
    for (ix, _) in enumerate(wNames):
        winsDiff = domMtx[ix]/domMtx[:,ix]
        tauW[ix] = winsDiff
    tauX = np.nan_to_num(tauW, 0)-1
    # Get sorting for most dominant -------------------------------------------
    if sorted:
        sorting = list(np.argsort([np.sum(r>0) for r in tauX]))[::-1]
        (tauS, namS) = (tauX[sorting][:,sorting], [wNames[i] for i in sorting])
    else:
        sorting = list(range(mSize))
        (tauS, namS) = (tauX, wNames)
    return (namS, tauS, sorting)


def calculateDominanceMatrixRatio(domMatrix, sorted=True):
    (mNames, mMatrix) = domMatrix
    tauW = np.zeros((len(mMatrix), len(mMatrix)))
    for (ix, _) in enumerate(mNames):
        winsDiff = mMatrix[ix]/mMatrix[:,ix]
        tauW[ix] = winsDiff
    tauX = np.copy(tauW)-1
    if sorted:
        sorting = list(np.argsort([np.sum(r>0) for r in tauX]))[::-1]
        tauS = tauX[sorting][:,sorting]
        namS = [mNames[i] for i in sorting]
    else:
        tauS = tauX
        namS = mNames
    return (namS, tauS)


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


def countDailyLobbies(btls):
    btlsFiltered = btls.copy()
    btlsFiltered['dummy'] = [1]*btlsFiltered.shape[0]
    gModes = sorted(list(btlsFiltered['mode'].unique()))
    counts = []
    for gMode in gModes:
        fltrs = (btlsFiltered['mode']==gMode, )
        fltrBool = [all(i) for i in zip(*fltrs)]
        btlsMode = btlsFiltered[fltrBool]
        c = btlsMode.groupby([btlsMode['period'].dt.date]).count()['dummy']
        c.name = gMode
        counts.append(c)
    df = pd.DataFrame(counts).fillna(0).T
    df.sort_index(inplace=True)
    return df


def smoothCountDailyLobbies(lbyDaily, gridSize=1000, sd=0.75):
    gModes = list(lbyDaily.columns)
    xys = [
        stt.gaussianSmooth(list(lbyDaily[gm]), gridSize=gridSize, sd=sd) 
        for gm in gModes
    ]
    return xys


def rankWeaponsFrequency(wpnFreq, wpnWLT):
    mNames = wpnWLT[0]
    wpnsNum = len(mNames)
    freqSorting = [mNames.index(w) for w in wpnFreq.keys()]
    wpnWinRatio = wpnWLT[1][:,0]/wpnWLT[1][:,2]
    # Weapons ranks triplets --------------------------------------------------
    wpnRanks = zip(
        [i+1 for i in range(wpnsNum)], 
        wpnFreq.keys(),
        [wpnWinRatio[ix] for ix in freqSorting]
    )
    return list(wpnRanks)


def getWeaponsDataframe(
        battlesResults,
        stats=['weapon', 'kill', 'assist', 'death', 'inked', 'special']
    ):
    dfs = []
    for prepend in ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']:
        df = battlesResults[[prepend+'-{}'.format(c) for c in stats]]
        df.columns = [c[3:] for c in df.columns]
        dfs.append(df)
    dfStats = pd.concat(dfs)
    return dfStats


def getWeaponStatsHistograms(
        weaponDF, range,
        stats=['kill', 'death', 'assist', 'special', 'inked'],
        normalized=True, binSize=1
    ):
    wpnHists = {
        stat: np.nan_to_num(
            stt.calcBinnedFrequencies(
                weaponDF[stat], range[0], range[1], 
                normalized=normalized, binSize=binSize
            ), 0
        )
        for stat in stats
    }
    return wpnHists


def getWeaponStatsMean(
        weaponDF,
        stats=['kill', 'death', 'assist', 'special', 'inked'],
        mFun=np.mean
    ):
    if weaponDF.shape[0] > 0:
        wpnMeans = {stat: mFun(weaponDF[stat]) for stat in stats}
    else:
        wpnMeans = {stat: 0 for stat in stats}
    return wpnMeans


def getWeaponsStatsHistograms(
        weaponsDF, weapons, range,
        stats=['kill', 'death', 'assist', 'special', 'inked'],
        normalized=True, binSize=1
    ):
    kFreqs = {}
    for wpn in weapons:
        wpnDF = weaponsDF[weaponsDF['weapon']==wpn]
        kFreqs[wpn] = getWeaponStatsHistograms(
            wpnDF, range, stats=stats, binSize=binSize, normalized=normalized
        )
    return kFreqs


def getWeaponsStatsSummary(
        weaponsDF, weapons, 
        summaryFunction=np.mean,
        stats=['kill', 'death', 'assist', 'special', 'inked']
    ):
    kMeans = {}
    for wpn in weapons:
        wpnDF = weaponsDF[weaponsDF['weapon']==wpn]
        kMeans[wpn] = getWeaponStatsMean(
            wpnDF, stats=stats, mFun=summaryFunction
        )
    return kMeans