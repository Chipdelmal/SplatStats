#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl
import numpy as np
from os import path
import pandas as pd
from termcolor import colored
from dateutil.parser import parse
import SplatStats.stats as stt
import SplatStats.Battle as bat
import SplatStats.parsers as par
import SplatStats.auxiliary as aux
import SplatStats.constants as cst


class Player:
    """
    Attributes
    ----------
    name : str
        Player's in-game name.
    id : int
        Player's in-game id.
    bPaths : list of paths
        List of paths for all the battle files to be analyzed.
    timezone : str
        Datetime-valid timezone string id for the player's location.
    battlesRecords : list of objects
        Full list of battle objects.
    battlesHistory : dataframe
        Full battle history.
    battlesHistoryByType : set of dataframes
        Battle history broken up by match types: "Turf War", "Rainmaker", "Splat Zones", "Clam Blitz", "Tower Control"
    playerStats : set
        Stats on full battle history.
    playerStatsByType : set of sets
        Stats on battle history by match-type
        
    Methods
    -------
    """
    ###########################################################################
    # Player info
    ###########################################################################
    def __init__(self, name, bPaths, id=None, timezone=None):
        self.name = name
        self.id = id
        self.bPaths = bPaths
        self.timezone = timezone
        # Parse player's battles dataframes -----------------------------------
        self.battleRecords = self.getBattleRecords()
        self.battlesHistory = self.parsePlayerHistoryFromBattles()
        self.battlesHistoryByType = self.getPlayerHistoryByTypes()
        # Assign stats --------------------------------------------------------
        self.playerStats = self.calcPlayerStats()
        self.playerStatsByType = self.calcPlayerStatsByTypes()

    ###########################################################################
    # Get battle records
    ###########################################################################    
    def getBattleRecords(self):
        fNum = len(self.bPaths)
        battleRecords = [None]*fNum
        for (ix, batFile) in enumerate(self.bPaths):
            battle = aux.loadBattle(batFile)
            battleRecords[ix] = battle
        return battleRecords

    def getBattleRecordsByType(self, battleType):
        battles = self.battlesHistory
        fltr = (battles['match type']==battleType)
        return battles[fltr]
        
    ###########################################################################
    # Get player history dataframe
    ###########################################################################
    def parsePlayerHistoryFromBattles(self, validOnly=True):
        battlesHistory = par.parsePlayerHistoryFromBattles(
            self.battleRecords, self.name, 
            validOnly=validOnly, timezone=self.timezone
        )
        self.battlesHistory = battlesHistory
        return self.battlesHistory
    
    def getPlayerHistoryByTypes(self):
        bTypes = cst.MATCH_TYPES
        bTypesHist = {
            bType: self.getBattleRecordsByType(bType) for bType in bTypes
        }
        return bTypesHist

    ###########################################################################
    # Calculate player stats from history dataframe
    ###########################################################################
    def calcPlayerStats(self):
        bHist = self.battlesHistory
        hStats = stt.calcBattleHistoryStats(bHist)
        return hStats
        
    def calcPlayerStatsByTypes(self):
        (bTypes, bHists) = (
            cst.MATCH_TYPES, 
            self.battlesHistoryByType
        )
        hStatsHist = {
            bType: stt.calcBattleHistoryStats(bHists[bType]) 
            for bType in bTypes if (bHists[bType].shape[0] > 0)
        }
        return hStatsHist