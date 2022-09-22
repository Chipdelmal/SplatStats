#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl
import numpy as np
from os import path
import pandas as pd
from termcolor import colored
from dateutil.parser import parse
import SplatStats.parsers as par
import SplatStats.auxiliary as aux
import SplatStats.constants as cst
import SplatStats.Battle as bat

class Player:
    """
    Attributes
    ----------
    name : str
        Player's in-game name
    id : int
        Player's in-game id
    battlesHistory : dataframe
        Player's full battle history
        
    Methods
    -------
    """
    ###########################################################################
    # Player info
    ###########################################################################
    def __init__(self, name, bPaths, id=None):
        self.name = name
        self.id = id
        self.bPaths = bPaths
        # Parse player's battles dataframe ------------------------------------
        self.battlesHistory = self.parsePlayerHistory()
    
    ###########################################################################
    # Get player history dataframe
    ###########################################################################
    def parsePlayerHistory(self, category='player name', validOnly=True):
        fNum = len(self.bPaths)
        playerDFs = []
        for (ix, batFile) in enumerate(self.bPaths):
            # Print progress --------------------------------------------------
            cpt = colored(f'* Loading History {ix+1:05d}/{fNum:05d}', 'red')
            print(cpt, end='\r')
            # Process battle --------------------------------------------------
            battle = aux.loadBattle(batFile)
            (rowA, rowE) = (
                battle.getAllyByCategory(self.name, category=category),
                battle.getEnemyByCategory(self.name, category=category)
            )
            # Append row to list ----------------------------------------------
            if rowA is not None:
                playerDFs.append(rowA)
            if rowE is not None:
                playerDFs.append(rowE)
        playerDF = pd.concat(playerDFs, axis=0)
        playerDF.astype(cst.BATTLE_DTYPES)
        # Re-arrange dataframe ------------------------------------------------
        playerDF.sort_values(by='datetime', inplace=True)
        playerDF.reset_index(drop=True, inplace=True)
        playerDF.drop([
            'player name', 'player name id', 'self'
        ], axis=1, inplace=True)
        playerDF.drop_duplicates(inplace=True)
        # Assign object to player's history -----------------------------------
        if validOnly:
            self.battlesHistory = playerDF[playerDF['win']!='NA']
        else:
            self.battlesHistory = playerDF
        return self.battlesHistory
    
    ###########################################################################
    # Calculate player stats from history dataframe
    ###########################################################################
    def calcPlayerStats(self):
        bHist = self.battlesHistory
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
        killsPerMinute = self.battlesHistory['kill']/matchDuration
        kpmAvg = np.mean(killsPerMinute)
        # Stats dictionary ----------------------------------------------------
        pStats = {
            # W/L stats
            'wl': {
                'win': wins, 'loss': loss, 'win ratio': winR
            },
            # KDASP stats
            'kdasp': {
                'kills': kTot, 'deaths': dTot, 'assists': aTot, 
                'special': sTot, 'paint': pTot 
            },
            'kdasp avg': {
                'kills': kAvg,  'deaths': dAvg, 'assist': aAvg,
                'special': sAvg, 'paint': pAvg,
            },
            # Special stats
            'other': {
                'kill ratio': killRatio, 'kills per minute': kpmAvg
            }
        }
        return pStats
        
