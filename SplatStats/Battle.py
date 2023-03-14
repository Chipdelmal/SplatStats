#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl
from os import path
import pandas as pd
from dateutil.parser import parse
import SplatStats.stats as stat
import SplatStats.parsers as par
import SplatStats.auxiliary as aux
pd.options.mode.chained_assignment = None

class Battle:
    """
    Attributes
    ----------
    id : str
        Battle's hash id.
    datetime : datetime
        Date/time at which the battle took place (zero timezone UTC).
    duration : int
        Duration of the match (in seconds).
    ko : bool
        Battle finished in KO?
    matchType: str
        Type of match ("Turf War", "Tower Control", "Rainkamer", "Splat Zones", "Clam Blitz").
    matchMode: str
        Used for splatfest identifier.
    festMatch: bool
        Determines if the match was a splatfest event.
    stage : str
        Stage's name.
    alliedTeam : dataframe
        Breakdown of the user's team.
    enemyTeams : list of dataframes
        Breakdown of the enemy teams.
    awards : list
        List of awards obtained in the battle.
    """
    ###########################################################################
    # Battle init
    ###########################################################################
    def __init__(self, battleDetail):
        # Battle info ---------------------------------------------------------
        self.id = battleDetail['id']
        self.matchType = battleDetail['vsRule']['name']
        self.matchMode = battleDetail['vsMode']['mode']
        self.festMatch = (True if self.matchMode=='FEST' else False)
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
        """Gets the player row given a team in the battle object.

        Args:
            name (str): Name of the player.
            team (dataframe): Team the player should be in.
            category (str, optional): _description_. Defaults to 'player name'.

        Returns:
            dataframe: Player's dataframe row that conforms to player history shape (see class' doc).
        """        
        # Filter player -------------------------------------------------------
        fltr = (team[category]==name)
        rowMatch = team[fltr]
        # Add flattenned battle info ------------------------------------------
        rowMatch['datetime'] = self.datetime
        rowMatch['ko'] = self.ko
        rowMatch['stage'] = self.stage
        rowMatch['match type'] = self.matchType
        rowMatch['duration'] = self.duration
        rowMatch['splatfest'] = self.festMatch
        rowMatch['match mode'] = self.matchMode
        # Add awards info -----------------------------------------------------
        if (rowMatch.shape[0]>0) and int(rowMatch['self']):
            awards = aux.awardsToStrings(self.awards)
            for i in range(len(awards)): 
                rowMatch[f'award_{i}'] = awards[i]
        # Return filtered row -------------------------------------------------
        return rowMatch
    
    def getAllyByCategory(self, name, category='player name'):
        """Returns an ally dataframe row filtering by a given category (usually 'name').

        Args:
            name (str or int): String or number to match in the category.
            category (str, optional): Category (column) name in the dataframe. Defaults to 'player name'.

        Returns:
            dataframe: Dataframe row that conforms to player history shape (see class' docs).
        """        
        pyr = self.getPlayerByCategory(name, self.alliedTeam, category=category)
        return pyr
    
    def getEnemyByCategory(self, name, category='player name'):
        """Returns an enemy dataframe row filtering by a given category (usually 'name').

        Args:
            name (str or int): String or number to match in the category.
            category (str, optional): Category (column) name in the dataframe. Defaults to 'player name'.

        Returns:
            dataframe: Dataframe row that conforms to player history shape (see class' docs).
        """        
        # Unsafe for tri-battles! check and fix later!
        pyrs = [
            self.getPlayerByCategory(name, eTeam, category=category)
            for eTeam in self.enemyTeams
        ][0]
        return pyrs
    
    def getAlliesAndEnemiesNames(self):
        """Returns a dictionary containing the names of allies and enemies.

        Returns:
            dict: Contains names of allies and enemies separated by key.
        """        
        aPlayers = list(self.alliedTeam['player name'])
        ePlayers = [list(e['player name']) for e in self.enemyTeams]
        pDict = {'allies': aPlayers, 'enemies': aux.flattenList(ePlayers)}
        return pDict
    
    def getFullRoster(self):
        """Generates the dataframe of all players involved in the battle.

        Returns:
            dataframe: Battle history dataframe with added team column.
        """        
        (alliedDF, enemyDF) = (
            self.alliedTeam,
            pd.concat(self.enemyTeams, axis=0)
        )
        alliedDF['Team'] = ['A']*alliedDF.shape[0]
        enemyDF['Team'] = ['E']*enemyDF.shape[0]
        df = pd.concat([alliedDF, enemyDF], axis=0).reset_index(drop=True)
        return df    
    
    def getAlliedTotal(
            self, 
            cats=['kill', 'death', 'assist', 'special', 'paint']
        ):
        """Get allied team total over selected categories.

        Args:
            cats (list, optional): Categories over which the data will be totaled. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].

        Returns:
            dict: Allied team totals over the categories.
        """        
        tTotal = stat.getTeamTotals(self.alliedTeam, cats=cats)
        return tTotal
    
    def getEnemiesTotals(
            self, 
            cats=['kill', 'death', 'assist', 'special', 'paint']
        ):
        """Get enemy teams total over selected categories.

        Args:
            cats (list, optional): Categories over which the data will be totaled. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].

        Returns:
            list of dataframes: Enemy team totals over the categories.
        """         
        teams = self.enemyTeams
        tTotals = [stat.getTeamTotals(team, cats=cats) for team in teams]
        return tTotals
    
    def getAlliedRanks(
            self,
            cats=['kill', 'death', 'assist', 'special', 'paint'],
            inverted=['death']
        ):
        """Returns a dataframe with the rankings of the allied players across categories (higher numbers being better unless in inverted list).


        Args:
            cats (list, optional): Categories over which the data will be totaled. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].
            inverted (list, optional): In the original rankings more is considered better, this list should contain the categories that should be inverted. Defaults to ['death'].


        Returns:
            dataframe: Allied team ranking dataframe over categories.
        """        
        team = self.alliedTeam
        ranks = stat.getTeamRanks(team, cats=cats, inverted=inverted)
        return ranks
    
    def getEnemiesRanks(
            self,
            cats=['kill', 'death', 'assist', 'special', 'paint'],
            inverted=['death']
        ):
        """Returns a list of dataframes with the rankings of the enemies players across categories (higher numbers being better unless in inverted list).

        Args:
            cats (list, optional): Categories over which the data will be totaled. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].
            inverted (list, optional): In the original rankings more is considered better, this list should contain the categories that should be inverted. Defaults to ['death'].

        Returns:
            list of dataframes: Enemy teams ranking dataframe over categories.
        """        
        dfRanks = []
        for team in self.enemyTeams:
            dfRank = stat.getTeamRanks(team, cats=cats, inverted=inverted)
            dfRanks.append(dfRank)
        return dfRanks

    def getFullRanks(
            self,
            cats=['kill', 'death', 'assist', 'special', 'paint'],
            inverted=['death']
        ):
        """Returns a dataframe with the rankings of the full roster of players across categories (higher numbers being better unless in inverted list).


        Args:
            cats (list, optional): Categories over which the data will be totaled. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].
            inverted (list, optional): In the original rankings more is considered better, this list should contain the categories that should be inverted. Defaults to ['death'].

        Returns:
            dataframe: Full roster ranking dataframe over categories.
        """        
        df = self.getFullRoster()
        dfRank = stat.getTeamRanks(df, cats=cats, inverted=inverted)
        return dfRank
        
    ###########################################################################
    # Export Methods
    ###########################################################################
    def dumpBattle(self, fPath='./', overwrite=True):
        """Serializes battle to disk with datetime as name.

        Args:
            fPath (str, optional): Path to which the object will be saved. Defaults to './'.

        Returns:
            str: Filepath to serialized battle.
        """        
        fName = aux.datetimeToString(self.datetime)
        bPath = path.join(fPath, f'{fName}.pkl')
        if (not path.isfile(bPath)) or overwrite:
            with open(bPath, 'wb') as f:
                pkl.dump(self, f)
        return bPath