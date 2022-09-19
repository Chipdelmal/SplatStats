#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl
from os import path
import pandas as pd
from dateutil.parser import parse
import SplatStats.parsers as par
import SplatStats.auxiliary as aux
pd.options.mode.chained_assignment = None

class Battle:
    """
    Attributes
    ----------
    id : str
        Battle's hash id
    datetime : datetime
        Date/time at which the battle took place (zero timezone UTC)
    duration : int
        Duration of the match (in seconds)
    ko : bool
        Battle finished in KO?
    matchType: str
        Type of match ("Turf War", "Tower Control", "Rainkamer"...)
    matchMode: str
        UNCLEAR
    festMatch: bool
        UNCLEAR
    stage : str
        Stage's name
    alliedTeam : dataframe
        Breakdown of the user's team
    enemyTeams : list of dataframes
        Breakdown of the enemy teams
        
    Methods
    -------
    dumpBattle(path="./"):
        Exports serialized battle object to disk.
    """
    ###########################################################################
    # Battle info
    ###########################################################################
    def __init__(self, battleDetail):
        # Battle info ---------------------------------------------------------
        self.id = battleDetail['id']
        self.festMatch = False
        self.matchType = battleDetail['vsRule']['name']
        self.matchMode = battleDetail['vsMode']['mode']
        self.stage = battleDetail['vsStage']['name']
        self.ko = aux.boolKO(battleDetail['knockout'])
        self.datetime = parse(battleDetail['playedTime'])
        self.duration = int(battleDetail['duration'])
        self.awards = par.parseAwards(battleDetail['awards'])
        # Get allied team details ---------------------------------------------
        myTeam = battleDetail['myTeam']
        self.alliedTeam = par.getTeamDataframe(myTeam, self.matchType)
        # Get enemy teams details ---------------------------------------------
        nTeams = len(battleDetail['otherTeams'])
        enemyTeams = [None]*nTeams
        for i in range(nTeams):
            eTeam = battleDetail['otherTeams'][i]
            enemyTeams[i] = par.getTeamDataframe(eTeam, self.matchType)
        self.enemyTeams = enemyTeams
        
    ###########################################################################
    # Filtering Methods
    ###########################################################################
    def getPlayerByCategory(self, name, team, category='player name'):
        # Filter player -------------------------------------------------------
        fltr = (team[category]==name)
        rowMatch = team[fltr]
        # Add flattenned battle info ------------------------------------------
        rowMatch['datetime'] = self.datetime
        rowMatch['ko'] = self.ko
        rowMatch['stage'] = self.stage
        rowMatch['match type'] = self.matchType
        rowMatch['duration'] = self.duration
        # Add awards info -----------------------------------------------------
        awards = aux.awardsToStrings(self.awards)
        for i in range(len(awards)):
            rowMatch[f'award_{i}'] = awards[i]
        # Return filtered row -------------------------------------------------
        return rowMatch
    
    def getAllyByCategory(self, name, category='player name'):
        py = self.getPlayerByCategory(name, self.alliedTeam, category=category)
        return py
    
    def getEnemyByCategory(self, name, category='player name'):
        pyrs = [
            self.getPlayerByCategory(name, eTeam, category=category)
            for eTeam in self.enemyTeams
        ]
        return pyrs
    
    ###########################################################################
    # Export Methods
    ###########################################################################
    def dumpBattle(self, fPath='./'):
        fName = aux.datetimeToString(self.datetime)
        with open(path.join(fPath, f'{fName}.pkl'), 'wb') as f:
            pkl.dump(self, f)