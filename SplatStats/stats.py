#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def calcBattleHistoryStats(bHist):
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
    (kAvg, dAvg, aAvg, sAvg, pAvg) = [
        i/matchNum for i in (kTot, dTot, aTot, sTot, pTot)
    ]
    # Win/lose stats (NA are loss) ----------------------------------------
    win  = [True if i=='W' else False for i in bHist['win']]
    wins = sum(win)
    winR = wins/len(win)
    loss = len(win)-wins
    # Ratios --------------------------------------------------------------
    killRatio = kTot/dTot
    (kpm, dpm, apm, spm, ppm) = [
        np.mean(bHist[i]/matchDuration) for i in cats
    ]
    # Stats dictionary ----------------------------------------------------
    pStats = {
        # W/L stats
        'general': {
            'total matches': matchNum,
            'win': wins, 'loss': loss, 
            'win ratio': winR, 'kill ratio': killRatio
        },
        # KPADS stats
        'kpads': {
            'kills': kTot, 'deaths': dTot, 'assists': aTot, 
            'special': sTot, 'paint': pTot 
        },
        'kpads avg': {
            'kills': kAvg,  'deaths': dAvg, 'assist': aAvg,
            'special': sAvg, 'paint': pAvg,
        },
        'kpads per min': {
            'kills': kpm, 'deaths': dpm, 'assist': apm,
            'special': spm, 'paint': ppm
        }
    }
    return pStats