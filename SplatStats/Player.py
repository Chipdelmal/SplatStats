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
        self.battleRecords = self.getBattleRecords()
        self.battlesHistory = self.parsePlayerHistoryFromBattles()
        # Assign stats --------------------------------------------------------
        self.playerStats = self.calcPlayerStats()

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

    ###########################################################################
    # Get player history dataframe
    ###########################################################################
    def parsePlayerHistoryFromBattles(self, validOnly=True):
        battlesHistory = par.parsePlayerHistoryFromBattles(
            self.battleRecords, self.name, validOnly=validOnly
        )
        self.battlesHistory = battlesHistory
        return self.battlesHistory
    
    ###########################################################################
    # Calculate player stats from history dataframe
    ###########################################################################
    def calcPlayerStats(self):
        bHist = self.battlesHistory
        hStats = stt.calcBattleHistoryStats(bHist)
        return hStats
        
