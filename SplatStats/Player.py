#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from tqdm import tqdm
from termcolor import colored
from collections import Counter
import SplatStats.stats as stt
import SplatStats.Battle as bat
import SplatStats.parsers as par
import SplatStats.auxiliary as aux
import SplatStats.constants as cst
import SplatStats.statInkConstants as ink


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
    """
    ###########################################################################
    # Player info
    ###########################################################################
    def __init__(self, name, bPaths, id=None, timezone=None, replaceNAN=True):
        self.name = name
        self.id = id
        self.bPaths = bPaths
        self.timezone = timezone
        # Parse player's battles dataframes -----------------------------------
        self.battleRecords = self.getBattleRecords()
        self.battlesHistory = self.parsePlayerHistoryFromBattles(replaceNAN=replaceNAN)
        self.battlesHistoryByType = self.getPlayerHistoryByTypes()
        # Assign stats --------------------------------------------------------
        self.playerStats = self.calcPlayerStats()
        self.playerStatsByType = self.calcPlayerStatsByTypes()

    ###########################################################################
    # Get battle records
    ###########################################################################    
    def getBattleRecords(self):
        """Loads all the battle files belonging to the player (bPaths) and assigns it to battleRecords.

        Returns:
            list: All battle objects loaded from files (see class' docs).
        """        
        fNum = len(self.bPaths)
        battleRecords = []
        cpt = colored(
            f'Reading battle object files from disk for {self.name}', 
            'red'
        )
        print(cpt, end='\r')
        for batFile in tqdm(self.bPaths):
            battle = aux.loadBattle(batFile)
            battleRecords.append(battle)
        return battleRecords

    ###########################################################################
    # Get player history dataframe
    ###########################################################################
    def parsePlayerHistoryFromBattles(
            self, validOnly=True, ammendWeapons=True, replaceNAN=True
        ):
        """Extracts the player's history from the battle records by matching the name in the dataframes.

        Args:
            validOnly (bool, optional): Filters out battles which didn't finish correctly (disconnects). Defaults to True.

        Returns:
            dataframe: Full battle history dataframe for the player, in which each row is the result of a match.
        """        
        battlesHistory = par.parsePlayerHistoryFromBattles(
            self.battleRecords, self.name, 
            validOnly=validOnly, timezone=self.timezone
        )
        battlesHistory['winBool'] = [1 if i=='W' else 0 for i in battlesHistory['win']]
        battlesHistory['loseBool'] = [1 if i=='L' else 0 for i in battlesHistory['win']]
        battlesHistory['participation'] = [1]*battlesHistory.shape[0]
        battlesHistory['kassist'] = (battlesHistory['kill']+0.5*battlesHistory['assist'])
        battlesHistory['kad'] = battlesHistory['kassist']/ [max(i, 1) for i in battlesHistory['death']]
        if replaceNAN:
            battlesHistory.replace([np.inf, np.nan, -np.inf], 0, inplace=True)
        if ammendWeapons:
            btlsHistoryDummy = battlesHistory.copy()
            for wpnTuple in ink.WPNS_REPLICAS:
                btlsHistoryDummy.replace(wpnTuple[0], wpnTuple[1], inplace=True)
            self.battlesHistory = btlsHistoryDummy
        else:
            self.battlesHistory = battlesHistory
        return self.battlesHistory
    
    def getPlayerHistoryByTypes(self):
        """Groups the player history into dictionary items corresponding to the match type played.

        Returns:
            dict of dataframes: Dictionary containing the different battle history dataframes.
        """        
        bTypes = cst.MATCH_TYPES
        bTypesHist = {
            bType: self.filterBattleHistoryWithType(bType) for bType in bTypes
        }
        return bTypesHist

    def filterBattleHistoryWithType(self, battleType):
        """Gets all the battles that match a certain battle type from a history dataframe.

        Args:
            battleType (str): String ID of the match type.

        Returns:
            dataframe: Filtered history dataframe containing only the matches of a certain type.
        """        
        battles = self.battlesHistory
        fltr = (battles['match type']==battleType)
        return battles[fltr]

    ###########################################################################
    # Calculate player stats from history dataframe
    ###########################################################################
    def calcPlayerStats(self):
        """Calculates and returns the stats for the player's battle history.

        Returns:
            dict: KPADS dictionary of stats.
        """        
        bHist = self.battlesHistory
        hStats = stt.calcBattleHistoryStats(bHist)
        return hStats
        
    def calcPlayerStatsByTypes(self):
        """Calculates and returns the stats for the player's battle history broken by match types.

        Returns:
            list: KPADS dictionaries of stats broken up by match type.
        """        
        (bTypes, bHists) = (
            cst.MATCH_TYPES, 
            self.battlesHistoryByType
        )
        hStatsHist = {
            bType: stt.calcBattleHistoryStats(bHists[bType]) 
            for bType in bTypes if (bHists[bType].shape[0] > 0)
        }
        return hStatsHist
    
    ###########################################################################
    # Get the names and counts of allies and enemies as appearing in battles
    ########################################################################### 
    def getAlliesAndEnemiesCounts(self):
        """Counts the number of times the player has been ally or faced a certain oponent.

        Returns:
            dict : Dictionary of counter objects containing the frequencies of matches with other players.
        """        
        bDetails = self.battleRecords
        (allies, enemies) = ([], [])
        for bDetail in bDetails:
            pDict = bDetail.getAlliesAndEnemiesNames()
            allies.append(pDict['allies'])
            enemies.append(pDict['enemies'])
        (allies, enemies) = [aux.flattenList(i) for i in (allies, enemies)] 
        (alliesC, enemiesC) = [
            Counter(i).most_common() for i in (allies, enemies)
        ]
        return {'allies': alliesC, 'enemies': enemiesC}
    
    ###########################################################################
    # Get award frequencies
    ###########################################################################
    def getAwardFrequencies(self):
        """Returns the frequencies of the awards obtained by the player.

        Returns:
            tuples: Sorted (award, frequency) tuples.
        """        
        awdsRaw = [
            list(self.battlesHistory['award_{}'.format(i)].dropna()) 
            for i in range(3)
        ]
        # Compile counter object 
        awds = []
        for awdRaw in awdsRaw:
            awdX = [i for i in awdRaw if type(i) is str]
            awd = [i.split('@')[0] for i in awdX]
            entry = [i.split('@') for i in awdX]
            # Count gold as double than silver
            centry = [[e[0], e[0]] if e[1]=='gold' else [e[0], ] for e in entry]
            awds.extend(centry)
        awdsFlat = [item for sublist in awds for item in sublist]
        awdsCount = Counter(awdsFlat).most_common()
        awdsCountNorm = [(i[0], i[1]/2) for i in awdsCount]
        return awdsCountNorm
    
    ###########################################################################
    # Get player rankings
    ########################################################################### 
    def getPlayerAlliedRanking(
            self,
            cats=['kill', 'death', 'assist', 'special', 'paint']
        ):
        """Calculates the ranking dataframe of the player with regards of allies on given categories.

        Args:
            cats (list, optional): Categories on the battleHistory upon which the ranking will be calculated. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].

        Returns:
            dataframe: Ranks dataframe by category.
        """        
        (name, btlRecords, battlesHistory) = (
            self.name, self.battleRecords, self.battlesHistory
            
        )

        rnks = []
        for btl in btlRecords[:]:
            dfA = btl.getAlliedRanks(cats=cats)
            dfE = pd.concat(btl.getEnemiesRanks(cats=cats))
            if name in set(dfA['player name']):
                fltr = dfA[dfA['player name'] == name]
                rnks.append(fltr)
            elif name in set(dfE['player name']):
                fltr = dfE[dfE['player name'] == name]
                rnks.append(fltr)
        df = pd.concat(rnks, axis=0).drop(columns=['player name', 'player name id'])
        # Filter invalid battles and make indexes match -----------------------
        bHist = battlesHistory
        vIx = list(bHist.index)
        df = df.iloc[vIx]
        df = df.set_index(pd.Series(vIx))
        df['datetime'] = bHist['datetime']
        return  df
    
    def getPlayerFullRanking(
            self,
            cats=['kill', 'death', 'assist', 'special', 'paint']
        ):
        """Calculates the ranking dataframe of the player with regards of all the players on given categories.

        Args:
            cats (list, optional): Categories on the battleHistory upon which the ranking will be calculated. Defaults to ['kill', 'death', 'assist', 'special', 'paint'].

        Returns:
            dataframe: Ranks dataframe by category.
        """     
        (btlRecords, rnks) = (self.battleRecords, [])
        for btl in btlRecords:
            df = btl.getFullRanks(cats=cats)
            fltr = df[df['player name'] == self.name]
            rnks.append(fltr)
        df = pd.concat(rnks, axis=0).drop(columns=['player name', 'player name id'])
        # Filter invalid battles and make indexes match -----------------------
        bHist = self.battlesHistory
        vIx = list(bHist.index)
        df = df.iloc[vIx]
        df = df.set_index(pd.Series(vIx))
        df['datetime'] = bHist['datetime']
        return  df