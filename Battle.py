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
        
    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """
    def __init__(self, battleDetail):
        #######################################################################
        # Battle info
        #######################################################################
        self.stage = battleDetail['vsStage']['name']
        self.ko = aux.boolKO(battleDetail['knockout'])
        self.datetime = parse(battleDetail['playedTime'])
        self.duration = int(battleDetail['duration'])
        #######################################################################
        # Get allied team details
        #######################################################################
        myTeam = battleDetail['myTeam']
        # Get players details -------------------------------------------------
        players = myTeam['players']
        playersInfo = par.getPlayersBattleInfo(players)
        # Add W/L column ------------------------------------------------------
        win = aux.boolWinLose(myTeam['judgement'])
        # Assign dataframe ----------------------------------------------------
        alliedDF = pd.DataFrame.from_dict(playersInfo)
        alliedDF['win'] = win
        self.alliedTeam = alliedDF
        #######################################################################
        # Get enemy teams details
        #######################################################################
        enemyTeams = []
        for i in range(len(battleDetail['otherTeams'])):
            eTeam = battleDetail['otherTeams'][i]
            ePlayers = eTeam['players']
            enemiesInfo = par.getPlayersBattleInfo(ePlayers)
            enemyTeams.append(pd.DataFrame.from_dict(enemiesInfo))
        self.enemyTeams = enemyTeams