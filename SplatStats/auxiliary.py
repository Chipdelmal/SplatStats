#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import dill as pkl
from os import path
from glob import glob
from collections import Counter


def gearPrepend(gearType):
    """Takes a gear type string as found in JSONs and standardizes it.

    Args:
        gearType (str): ID string of the type of gear.

    Returns:
        str: Standardized gear string
    """    
    if (gearType=='headGear'):
        gPrep = 'head'
    elif (gearType=='clothingGear'):
        gPrep = 'shirt'
    elif (gearType=='shoesGear'):
        gPrep = 'shoes'
    return gPrep


def boolWinLose(winString):
    """Shortens and standardizes the win/lose string from JSONs.

    Args:
        winString (str): Win/lose string in long form.

    Returns:
        str: W/L string in shortform
    """    
    if winString=='WIN':
        wBool = 'W'
    elif winString == 'LOSE':
        wBool = 'L'
    else:
        wBool = 'NA'
    return wBool


def boolKO(koString):
    """Converts the KO string in the JSONs to a bool.

    Args:
        koString (str): KO string

    Returns:
        bool: KO value either in win or lose condition.
    """    
    if (koString == 'WIN') or (koString == 'LOSE'):
        koBool = True
    else:
        koBool = False
    return koBool


def datetimeToString(datetime):
    """Converts a datetime object into a standardized string form.

    Args:
        datetime (datetime): Standard datetime object to format into string.

    Returns:
        str: Standardized datetime string in the form "Y_M_D-Hhm"
    """    
    return datetime.strftime("%Y_%m_%d-%Hh%M")


def loadBattle(fPath):
    """Reads a pickled battle file from disk.

    Args:
        fPath (filepath): Full path in which the battle pkl file can be found.

    Returns:
        object: Battle object (see class' docs)
    """    
    with open(fPath, 'rb') as f:
        battle = pkl.load(f)
    return battle


def loadBattlesFromFiles(bPaths):
    """Loads battle objects from disk without the need to generate a Player object.

    Args:
        bPath (str): Path to the folder from where the battle files will be loaded.

    Returns:
        list: List of battle objects.
    """    
    bObjList = [loadBattle(bPath) for bPath in bPaths]
    return bObjList


def getPlayerCountsInBattles(battles):
    """Gets the player appearance counts from a list of battle objects (ally and enemy combined).

    Args:
        battles (list): List of battle objects (see "loadBattlesFromFiles")

    Returns:
        list: Counter object list with player appearance counts sorted by value.
    """    
    playersNames = []
    for battle in battles:
        ae = battle.getAlliesAndEnemiesNames()
        playersNames.extend(ae['allies'])
        playersNames.extend(ae['enemies'])
    pCount = Counter(playersNames).most_common()
    return pCount



def getHistoryFolders(histPath, fldrPat='export-*'):
    """Parses the folder paths for all instances matching a pattern (used to find JSON files folders).

    Args:
        histPath (path): Full basepath in which all the folders are stored.
        fldrPat (str, optional): Glob pattern to match in searching for folder names. Defaults to 'export-\*'.

    Returns:
        list: Unsorted list of folders that match the glob pattern.
    """    
    histFolders = glob(path.join(histPath, fldrPat))
    return histFolders


def getHistoryFiles(histFolders, pattern='results.json'):
    """Given a list of folders, it looks for matches in filenames.

    Args:
        histFolders (list): List of folder paths to search for matches in.
        pattern (str, optional): Glob pattern for filenames matches. Defaults to 'results.json'.

    Returns:
        list: Full filepaths for all the glob file matches.
    """    
    histFiles = []
    for f in histFolders:
        histFiles.extend(glob(path.join(f, pattern)))
    return histFiles


def awardsToStrings(awardsDF, sep='@'):
    """Condenses an awards dataframe into a list of strings for easier handling in player's history.

    Args:
        awardsDF (dataframe): Dataframe of awards as parsed from JSON files.
        sep (str, optional): Separator character for strings elements. Defaults to '@'.

    Returns:
        list: List of award strings.
    """    
    awds = []
    for i in range(awardsDF.shape[0]):
        row = awardsDF.iloc[i]
        awds.append(f"{row['name']}{sep}{row['rank']}{sep}{row['place']}")
    return awds
    
flattenList = lambda irregular_list:[element for item in irregular_list for element in flattenList(item)] if type(irregular_list) is list else [irregular_list]


def isNotebook():
    """Detects if the file is being run as a jupyter notebook (for dev purposes).

    Returns:
        bool: Is true if the file is being run in an interactive session.
    """    
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def alphaToHex(alphaFloat):
    xInter = np.interp(alphaFloat, (0, 1), (0, 255))
    xHex = hex(int(xInter))
    return xHex[2:]
