#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import warnings
from os import path
import pandas as pd
from glob import glob
from termcolor import colored
from dateutil.parser import parse
import SplatStats.constants as cst
import SplatStats.auxiliary as aux
import SplatStats.Battle as bat
warnings.simplefilter(action='ignore', category=FutureWarning)

class History:
    """
    Attributes
    ----------
    historyFiles : list of paths
        List of battle history filepaths

    Methods
    -------
    """
    ###########################################################################
    # History info
    ###########################################################################
    def __init__(self, iPath, oPath):
        self.outputPath = oPath
        self.inputPath = iPath
        # Get history filepaths -----------------------------------------------
        hFolders = aux.getHistoryFolders(iPath, fldrPat='export-*')
        hFiles = aux.getHistoryFiles(hFolders, pattern='results.json')
        self.historyFiles = hFiles
        # Start the battle files list as empty --------------------------------
        # self.dumpBattlesFromJSONS()
        # self.getBattleFilepaths()

    ###########################################################################
    # Dump all battles
    ###########################################################################
    def dumpBattlesFromJSONS(self):
        fNum = len(self.historyFiles)
        for (ix, fName) in enumerate(self.historyFiles):
            # Print progress --------------------------------------------------
            cpt = colored(f'* Parsing JSONs {ix+1:05d}/{fNum:05d}', 'red')
            print(cpt, end='\r')
            # Load JSON -------------------------------------------------------
            with open(fName, 'r') as file:
                data = json.load(file)
            # Process battles in file -----------------------------------------
            histSize = len(data)
            for i in range(histSize):
                bDetail = data[i]['data']['vsHistoryDetail']
                # Process battle history --------------------------------------
                battle = bat.Battle(bDetail)
                # Export battle history ---------------------------------------
                battle.dumpBattle(self.outputPath)
                
    ###########################################################################
    # Get battle filepaths
    ###########################################################################
    def getBattleFilepaths(self):
        battleFilepaths = glob(path.join(self.outputPath, '*.pkl'))
        self.battleFilepaths = battleFilepaths
        
    ###########################################################################
    # Get player history dataframe
    ###########################################################################
    def getPlayerHistory(self, playerName, category='player name'):
        fNum = len(self.battleFilepaths)
        playerDFs = []
        for (ix, batFile) in enumerate(self.battleFilepaths):
            # Print progress --------------------------------------------------
            cpt = colored(f'* Loading History {ix+1:05d}/{fNum:05d}', 'red')
            print(cpt, end='\r')
            # Process battle --------------------------------------------------
            battle = aux.loadBattle(batFile)
            rowA = battle.getAllyByCategory(playerName, category=category)
            rowE = battle.getEnemyByCategory(playerName, category=category)
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
    