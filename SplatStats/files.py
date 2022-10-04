
import json
import warnings
from os import path
from glob import glob
from tqdm import tqdm
from termcolor import colored
import SplatStats.Battle as bat
import SplatStats.auxiliary as aux
warnings.simplefilter(action='ignore', category=FutureWarning)

###########################################################################
# Dump all battles
###########################################################################
def dumpBattlesFromJSONS(historyFilepaths, oPath):
    """Takes a list of s3s "results.json" filepaths, converts them into batle objects and serializes them to disk.
    
    Args:
        historyFilepaths (list): List of "results.json" filepaths (use "getDataFilepaths")
        oPath (str): Path in which the battle pkl files will be stored.

    Returns:
        list: List of filepaths to battle files.
    """    
    (hFiles, fNum) = (historyFilepaths, len(historyFilepaths))
    bPaths = []
    cpt = colored(f'Parsing JSONs to battle object files (pkl)', 'red')
    print(cpt, end='\r')
    for fName in tqdm(hFiles):
        # Load JSON -------------------------------------------------------
        with open(fName, 'r') as file:
            data = json.load(file)
        # Process battles in file -----------------------------------------
        histSize = len(data)
        for i in range(histSize):
            bDetail = data[i]['data']['vsHistoryDetail']
            # Process battle history --------------------------------------
            battle = bat.Battle(bDetail)
            # Export battle history ---------------------------------------
            bPath = battle.dumpBattle(oPath)
            bPaths.append(bPath)
    return bPaths
        
###########################################################################
# Get filepaths
###########################################################################
def getDataFilepaths(iPath, fldrPat='export-*', filePat='results.json'):
    """Gets the filepaths in which files with a certain pattern can be found inside folders with a given pattern.

    Args:
        iPath (str): Base path in which we will perform the folders search.
        fldrPat (str, optional): Glob pattern for folder matches. Defaults to 'export-\*'.
        filePat (str, optional): Glob pattern for file matches inside the folders. Defaults to 'results.json'.

    Returns:
        list: List of filepaths that match the provided patterns.
    """    
    hFolders = aux.getHistoryFolders(iPath, fldrPat=fldrPat)
    hFiles = aux.getHistoryFiles(hFolders, pattern=filePat) 
    return hFiles


def getBattleFilepaths(bPath, filePat='*.pkl'):
    """Parses all the battle files from a folder.

    Args:
        bPath (str): Path to the folder from where the battle files will be loaded.
        filePat (str, optional): Pattern to match for in filenames. Defaults to '\*.pkl'.

    Returns:
        list: Filepaths to battle files.
    """    
    battleFilepaths = glob(path.join(bPath, filePat))
    return battleFilepaths

