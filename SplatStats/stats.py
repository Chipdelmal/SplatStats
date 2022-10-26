#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy.stats as sts


def calcBattleHistoryStats(bHist, kassistWeight=0.5):
    """Calculates the basic player stats for a battle history dataframe.

    Args:
        bHist (dataframe): Battle history dataframe for a player.

    Returns:
        dict: Stats (kills, paint, assists, deaths, specials) in normal, average, and per minute forms.
    """    
    # Getting constants ---------------------------------------------------
    matchNum = bHist.shape[0]
    matchDuration = (bHist['duration']/60)
    # Getting counts ------------------------------------------------------
    cats = ('kill', 'death', 'assist', 'special', 'paint')
    (kCnt, dCnt, aCnt, sCnt, pCnt) = [bHist[cat] for cat in cats]
    # Kill/Death/Assist/Paint stats ---------------------------------------
    (kTot, dTot, aTot, sTot, pTot) = [
        sum(i) for i in (kCnt, dCnt, aCnt, sCnt, pCnt)
    ]
    kaTot = kTot + (kassistWeight*aTot)
    (kAvg, dAvg, aAvg, sAvg, pAvg) = [
        i/matchNum for i in (kTot, dTot, aTot, sTot, pTot)
    ]
    kaAvg = (kaTot/matchNum)
    # Win/lose stats (NA are loss) ----------------------------------------
    win  = [True if i=='W' else False for i in bHist['win']]
    wins = sum(win)
    winR = wins/len(win)
    loss = len(win)-wins
    # Ratios --------------------------------------------------------------
    killRatio = kTot/dTot
    kallRatio = kaTot/dTot
    (kpm, dpm, apm, spm, ppm) = [
        np.mean(bHist[i]/matchDuration) for i in cats
    ]
    kallpm = np.mean(
        (bHist['kill']+kassistWeight*bHist['assist'])/matchDuration
    )
    # Stats dictionary ----------------------------------------------------
    pStats = {
        # W/L stats
        'general': {
            'total matches': matchNum, 'paint': pTot,
            'win': wins, 'loss': loss,
            'win ratio': winR, 'kill ratio': killRatio, 
            'kassists ratio': kallRatio
        },
        # KPADS stats
        'kpads': {
            'kills': kTot, 'deaths': dTot, 'assists': aTot, 
            'special': sTot, 'paint': pTot, 'kassists': kaTot
        },
        'kpads avg': {
            'kills': kAvg,  'deaths': dAvg, 'assists': aAvg,
            'special': sAvg, 'paint': pAvg, 'kassists': kaAvg
        },
        'kpads per min': {
            'kills': kpm, 'deaths': dpm, 'assists': apm,
            'special': spm, 'paint': ppm, 'kassists': kallpm
        }
    }
    return pStats


def frequencyInRange(array, xMin, xMax):
    """Calculates the number of entries of an array that fall within the defined range.

    Args:
        array (array): Array from which the frequencies will be calculated.
        xMin (float): Lower bound of the range for the count (inclusive).
        xMax (float): Upper bound of the range for the count (non-inclusive).

    Returns:
        int: Frequency of occurrences that fall within the range.
    """    
    count = 0
    for n in array:
        if (xMin <= n) and (n < xMax):
            count += 1
    return count

def calcBinnedFrequencies(array, xMin, xMax, binSize=1, normalized=False):
    """Calculates the binned frequencies of numbers in the array in the ranges defined.

    Args:
        array (array): Array from which all the frequencies will be calculated.
        xMin (int): Lowest possible value that will be counted.
        xMax (int): Highest possible value that will be counted.
        binSize (int, optional): Step size for the binning (from xMin to xMax in intervals of binSize). Defaults to 1.
        normalized (bool, optional): If true, the frequencies are divided by the total so that they sum to 1. Defaults to False.

    Returns:
        array: Frequencies of ocurrences in the defined ranges.
    """    
    freqs = np.array([
        frequencyInRange(array, i, i+binSize) for i in 
        range(xMin, xMax, binSize)
    ])
    total = np.sum(freqs)
    if normalized:
        freqs = freqs/total
    return freqs


def calcStatsByKey(bHist, key, sortBy='win ratio', ascending=False):
    """Given a battle history dataframe, this function calculates stats broken down by the supplied key (column).

    Args:
        bHist (dataframe): Battle history dataframe for a player.
        key (str, optional): Column name on the dataframe upon that will work as the grouping element for stats. Defaults to 'stage'.
        sortBy (str, optional): Sorting key for the output dataframe (no sorting if False). Defaults to 'win ratio'.
        ascending (bool, optional): Ascending or descending order for sorting. Defaults to False.

    Returns:
        dataframe: Stats over provided key (general, kpads, kpads avg, kpads per min)
    """
    (statsByStage, stages) = ({}, list(set(bHist[key])))
    for st in stages:
        # Filter sub dataframe by stage -----------------------------------
        df_fltrd = bHist[bHist[key]==st]
        stageDict = calcBattleHistoryStats(df_fltrd)
        # Add key to main dictionary
        statsByStage[st] = stageDict
    # Flatten the dictionaries into a dataframe ---------------------------
    dList = []
    for st in stages:
        # Flatten the dictionary
        row = statsByStage[st]
        (avg, xpm) = (
            {k+' avg':row['kpads avg'][k] for k in row['kpads avg']},
            {k+' prm':row['kpads per min'][k] for k in row['kpads per min']}
        )
        dictsCombo = (
            {key: st} | row['general'] | row['kpads'] | avg | xpm
        )
        dList.append(dictsCombo)
    df = pd.DataFrame(dList)
    if sortBy:
        df.sort_values(sortBy, ascending=ascending, inplace=True)
    return df


def calcStagesStats(bHist, sortBy='win ratio', ascending=False):
    """Given a battle history dataframe, this function calculates the stats broken down by stage and returns them as a dataframe (legacy wrapper for 'calcStatsByKey').

    Args:
        bHist (dataframe): Battle history dataframe for a player.
        key (str, optional): Column name on the dataframe upon that will work as the grouping element for stats. Defaults to 'stage'.
        sortBy (str, optional): Sorting key for the output dataframe (no sorting if False). Defaults to 'win ratio'.
        ascending (bool, optional): Ascending or descending order for sorting. Defaults to False.

    Returns:
        dataframe: Stats over stages (general, kpads, kpads avg, kpads per min)
    """    
    df = calcStatsByKey(
        bHist, key='stage', sortBy=sortBy, ascending=ascending
    )
    return df


def calcStagesStatsByType(bHist):
    """Given a battle history dataframe, this function calculates the stats broken down by match type and stage; and returns them as a dictionary of dataframes.

    Args:
        bHist (dataframe): Battle history dataframe for a player.

    Returns:
        dict: Dictionary of dataframes where the key is the match type, and the dataframe is calculated with 'calcStagesStats'.
    """    
    (matchDFs, matchTypes) = ({}, list(set(bHist['match type'])))
    for mt in matchTypes:
        # Filter dataframe by match type --------------------------------------
        subDF = bHist[bHist['match type']==mt]
        df = calcStagesStats(subDF)
        # Add the dataframe to the dictionary of match types ------------------
        matchDFs[mt] = df
    return matchDFs


def getTeamTotals(
        teamDF, 
        cats=['kill', 'death', 'assist', 'special', 'paint']
    ):
    """Get the team total over the selected categories.

    Args:
        teamDF (dataframe): Team battle dataframe.
        cats (list, optional): Categories over which the data will be totaled. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].

    Returns:
        dict: Team totals over the categories.
    """    
    dfSum = teamDF[cats].sum()
    dfSumDict = dict(dfSum)
    return dfSumDict


def getTeamRanks(
        teamDF,
        cats=['kill', 'death', 'assist', 'special', 'paint'],
        inverted=['death']
    ):
    """Returns a dataframe with the rankings of the players in the dataframe across categories (higher numbers being better unless in inverted list).

    Args:
        teamDF (dataframe): Team battle dataframe.
        cats (list, optional): Categories over which the data will be totaled. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].
        inverted (list, optional): In the original rankings more is considered better, this list should contain the categories that should be inverted. Defaults to ['death'].

    Returns:
        dataframe: Team ranking dataframe over categories.
    """    
    team = teamDF
    # Get names and ranks of the players --------------------------------------
    (names, ranks) = (
        team[['player name', 'player name id']],
        team[cats].rank(ascending=False).astype(int)
    )
    dfRank = pd.concat([names, ranks], axis=1)
    # Invert the rankings of needed columns -----------------------------------
    pNums = dfRank.shape[0]+1
    for cat in inverted:
        dfRank[cat] = pNums-dfRank[cat]
    return dfRank


def aggregateStatsByPeriod(playerHistory, period='h'):
    """Sums the stats over a given period of time.

    Args:
        playerHistory (dataframe): Player history dataframe.
        period (str, optional): Time period over which the stats will be aggregated. Defaults to 'h'.

    Returns:
        dataframe: Dataframe of states where the rows are the beginning of the periods.
    """    
    # Add the number of matches and wins
    playerHistory['matches'] = [1]*playerHistory.shape[0]
    playerHistory['win bool'] = np.asarray(
        [i=='W' for i in playerHistory['win']]
    )
    # Re-shape to new period
    periodHistory = playerHistory.groupby(
        playerHistory['datetime'].dt.floor(period)
    ).sum()
    periodHistory.rename(columns={'win bool': 'win'}, inplace=True)
    return periodHistory
    
    
def gaussianSmooth(y, gridSize=500, sd=1):
    """Performs a gaussian smoothing process upon the provided data.

    Args:
        y (np array): Values of the signal to be smoothed.
        gridSize (int, optional): Number of samples in the x range. Defaults to 500.
        sd (int, optional): Standard deviation for the smoothing process. Defaults to 1.

    Returns:
        list of np arrays: Smoothed values over the provided X range.
    """
    x = range(y.shape[0])
    grid = np.linspace(min(x), max(x), num=gridSize)
    weights = np.transpose([sts.norm.pdf(grid, m, sd) for m in x])
    weights = weights / weights.sum(0)
    smoothed = (weights*y).sum(1)
    return (grid, smoothed)


def windowAverage(data, kernelSize=5, mode='valid'):
    """Calculates the window average on the data array.

    Args:
        data (np array): Data on which the window average will be calculated.
        kernelSize (int, optional): . Defaults to 5.
        mode (str, optional): Size of the output array as accepted by np.convolve {'full', 'valid', 'same'}. Defaults to 'valid'.

    Returns:
        np array: Window-averaged data array.
    """    
    kernel = np.ones(kernelSize)/kernelSize
    dataConvolved = np.convolve(data, kernel, mode=mode)
    return dataConvolved