#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
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
        """Loads all the battle files belonging to the player (bPaths) and assigns it to battleRecords.

        Returns:
            list: All battle objects loaded from files (see class' docs).
        """        
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
        (alliesC, enemiesC) = [Counter(i) for i in (allies, enemies)]
        alliesC.pop(self.name)
        return {'allies': alliesC, 'enemies': enemiesC}