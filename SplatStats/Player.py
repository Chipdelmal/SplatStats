#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl
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
    def __init__(self, name, id=None):
        self.name = name
        self.id = id
        self.battlesHistory = None
    
    ###########################################################################
    # Get player history dataframe
    ###########################################################################
    def getPlayerHistory(self, bPaths, category='player name'):
        fNum = len(bPaths)
        playerDFs = []
        for (ix, batFile) in enumerate(bPaths):
            # Print progress --------------------------------------------------
            cpt = colored(f'* Loading History {ix+1:05d}/{fNum:05d}', 'red')
            print(cpt, end='\r')
            # Process battle --------------------------------------------------
            battle = aux.loadBattle(batFile)
            (rowA, rowE) = (
                battle.getAllyByCategory(self.playerName, category=category),
                battle.getEnemyByCategory(self.playerName, category=category)
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
        return  playerDF
    