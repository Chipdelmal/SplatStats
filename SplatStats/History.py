#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import warnings
import dill as pkl
from os import path
import pandas as pd
from glob import glob
from dateutil.parser import parse
import SplatStats.Battle as bat
import SplatStats.parsers as pa
import SplatStats.constants as cst
import SplatStats.auxiliary as aux
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
        hFolders = aux.getHistoryFolders(iPath, expPat='export-*')
        hFiles = aux.getHistoryFiles(hFolders, pattern='results.json')
        self.historyFiles = hFiles
        # Start the battle files list as empty --------------------------------
        self.dumpBattlesFromJSONS()
        self.getBattleFilepaths()

    ###########################################################################
    # Dump all battles
    ###########################################################################
    def dumpBattlesFromJSONS(self):
        for fName in self.historyFiles:
            with open(fName, 'r') as file:
                data = json.load(file)
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
        playerDFs = []
        for batFile in self.battleFilepaths:
            battle = aux.loadBattle(batFile)
            rowA = battle.getAllyByCategory(playerName, category=category)
            rowE = battle.getEnemyByCategory(playerName, category=category)
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
    