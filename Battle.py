#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dateutil.parser import parse
import pandas as pd
import parsers as par
import auxiliary as aux

class Battle:
    """
    Attributes
    ----------
    alliedTeam : dataframe
        Breakdown of the user's team
    enemyTeams : list of dataframes
        Breakdown of the enemy teams
    datetime : datetime
        Date/time at which the battle took place
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
        
    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """
    def __init__(self, battleDetail):
        #######################################################################
        # Battle info
        #######################################################################
        self.festMatch = False
        self.matchType = battleDetail['vsRule']['name']
        self.matchMode = battleDetail['vsMode']['mode']
        self.stage = battleDetail['vsStage']['name']
        self.ko = aux.boolKO(battleDetail['knockout'])
        self.datetime = parse(battleDetail['playedTime'])
        self.duration = int(battleDetail['duration'])
        #######################################################################
        # Get allied team details
        #######################################################################
        myTeam = battleDetail['myTeam']
        self.alliedTeam = par.getTeamDataframe(myTeam, self.matchType)
        #######################################################################
        # Get enemy teams details
        #######################################################################
        nTeams = len(battleDetail['otherTeams'])
        enemyTeams = [None]*nTeams
        for i in range(nTeams):
            eTeam = battleDetail['otherTeams'][i]
            enemyTeams[i] = par.getTeamDataframe(eTeam, self.matchType)
        self.enemyTeams = enemyTeams
        
