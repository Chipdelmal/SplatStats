#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from termcolor import colored
import SplatStats.auxiliary as aux
import SplatStats.constants as cst

def getPlayerWeapon(player):
    """Extracts the weapons elements from the player JSON dictionary.

    Args:
        player (dict): Player dictionary as extrated from JSON.

    Returns:
        dict: Standardized weapon dictionary.
    """    
    pWeapon = player['weapon']
    wDict = {
        'main weapon': pWeapon['name'], 
        'sub weapon': pWeapon['subWeapon']['name'], 
        'special weapon': pWeapon['specialWeapon']['name']
    }
    return wDict

def getPlayerResults(player):
    """Extracts the KADS elements from the player JSON dictionary.

    Args:
        player (dict): Player dictionary as extracted from JSON.

    Returns:
        dict: KADS dictionary
    """    
    pResult = player['result']
    if pResult:
        pResults = {
            k: pResult[k] for k in ('kill', 'death', 'assist', 'special')
        }
    else:
        pResults = {
            'kill': 0, 'death': 0, 'assist': 0, 'special': 0
        }
    return pResults

def getGearUnit(player, gType='headGear'):
    """Extracts the gear elements from the player JSON dictionary.

    Args:
        player (dict): Player dictionary as extracted from JSON.
        gType (str, optional): _description_. Defaults to 'headGear'.

    Returns:
        dict: Standardized gear dictionary for a given set (head, clothing, shoes).
    """    
    gear = player[gType]
    gPrep = aux.gearPrepend(gType)
    keyPat = [
        f'{gPrep} {s}' for s in ['name', 'main', 'sub_0', 'sub_1', 'sub_2']
    ]
    adPow = dict.fromkeys(keyPat)
    adPow[f'{gPrep} name'] = gear['name']
    adPow[f'{gPrep} main'] = gear['primaryGearPower']['name']
    for (i, g) in enumerate(gear['additionalGearPowers']):
        adPow[f'{gPrep} sub_{i}'] = g['name']
    return adPow

def getGear(player):
    """Extracts the full gear elements from the player JSON dictionary.

    Args:
        player (dict): Player dictionary as extracted from JSON.

    Returns:
        dict: Standardized gear dictionary.
    """    
    gearTypes = ('headGear', 'clothingGear', 'shoesGear')
    (headDict, clothesDict, shoesDict) = [
        getGearUnit(player, gType) for gType in gearTypes
    ]
    return {**headDict, **clothesDict, **shoesDict}

def getPlayersBattleInfo(players):
    """Players JSON object.

    Args:
        players (dict): Players dictionary as parsed from JSON.

    Returns:
        dict: Player info dictionary.
    """    
    playersInfo = [None]*len(players)
    for (pix, player) in enumerate(players):
        # Condensed Info ------------------------------------------------------
        resultsDict = getPlayerResults(player)
        weaponsDict = getPlayerWeapon(player)
        gearDict = getGear(player)
        # Dictionary ----------------------------------------------------------
        pDict = {
            'player name': player['name'], 
            'player name id': player['nameId'], 
            **weaponsDict,
            **resultsDict, 
            'paint': player['paint'],
            **gearDict,
            'self': player['isMyself']
            # 'player id': player['id']
        }
        playersInfo[pix] = pDict
    return playersInfo

def getMatchScore(teamResult, matchType):
    """From the teamResult JSON structure and match type, selects which score should be parsed.

    Args:
        teamResult (dict): JSON dictionary of team results.
        matchType (str): String ID of the match type.

    Returns:
        float/int/bool: Score of the match (false if the match didn't finish correctly).
    """    
    # Check it the match finished correctly
    if teamResult:
        # If the match was "turf", then the score is paint
        if matchType == 'Turf War':
            return teamResult['paintRatio']
        else: 
            return teamResult['score']
    else:
        return False
    
def getTeamDataframe(team, matchType):
    """Compiles a consistent dataframe from the JSON structured team result structure.

    Args:
        team (dict): JSON-original team dictionary of results.
        matchType (str): Match type ID of the battle.

    Returns:
        dataframe: Standardized battle results dataframe.
    """    
    # Get players details -----------------------------------------------------
    players = team['players']
    playersInfo = getPlayersBattleInfo(players)
    # Add W/L column ----------------------------------------------------------
    win = aux.boolWinLose(team['judgement'])
    # Add score ---------------------------------------------------------------
    scoreInfo = getMatchScore(team['result'], matchType)
    # Assign dataframe --------------------------------------------------------
    alliedDF = pd.DataFrame.from_dict(playersInfo)
    alliedDF['win'] = win
    alliedDF['score'] = scoreInfo
    return alliedDF

def parseAwards(awardsList):
    """Converts the awards list from the JSON structure into a dataframe.

    Args:
        awardsList (list): List of awards from JSON format.

    Returns:
        dataframe: Dataframe structure with name, place and rank for awards.
    """    
    awards = []
    for aw in awardsList:
        (name, rank) = (aw['name'], aw['rank'])
        if name[0]=='#':
            awards.append({
                'place': name[1:2], 'name': name[3:], 'rank': rank.lower()
            })
        else:
            awards.append({
                'place': '0', 'name': name[:], 'rank': rank.lower()
            })  
    awardsDF = pd.DataFrame.from_dict(awards)
    return awardsDF


def parsePlayerHistoryFromBattles(
        battleRecords, name, category='player name', 
        validOnly=True, timezone=None
    ):
    """Gets the history dataframe for a player, given a list of battle records and the name of the player.

    Args:
        battleRecords (list): List of battle objects to process.
        name (str): Name of the player.
        category (str, optional): Could be used to filter player by ID in the future (unused). Defaults to 'player name'.
        validOnly (bool, optional): Get only the matches that finished correctly (no disconnects or errors). Defaults to True.
        timezone (_type_, optional): Timezone in which the player played the matches. Defaults to None.

    Returns:
        dataframe: Full player history dataframe (check class' docs).
    """    
    battles = battleRecords
    playerDFs = []
    for (ix, battle) in enumerate(battles):
        # Print progress ------------------------------------------------------
        # cpt = colored(f'* Processing History {ix+1:05d}/{fNum:05d}', 'blue')
        # print(cpt, end='\r')
        # Process battle ------------------------------------------------------
        (rowA, rowE) = (
            battle.getAllyByCategory(name, category=category),
            battle.getEnemyByCategory(name, category=category)
        )
        # Append row to list --------------------------------------------------
        if rowA is not None:
            playerDFs.append(rowA)
        if rowE is not None:
            playerDFs.append(rowE)
    playerDF = pd.concat(playerDFs, axis=0)
    playerDF.astype(cst.BATTLE_DTYPES)
    # Re-arrange dataframe ----------------------------------------------------
    playerDF.sort_values(by='datetime', inplace=True)
    playerDF.reset_index(drop=True, inplace=True)
    playerDF.drop([
        'player name', 'player name id', 'self'
    ], axis=1, inplace=True)
    playerDF.drop_duplicates(inplace=True)
    # Fix timezone ------------------------------------------------------------
    if timezone:
        playerDF['datetime'] = playerDF['datetime'].dt.tz_convert(timezone)
    # Assign object to player's history ---------------------------------------
    if validOnly:
        bHist = playerDF[playerDF['win']!='NA']
    else:
        bHist = playerDF
    return bHist