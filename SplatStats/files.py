
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
def dumpBattlesFromJSONS(historyFilepaths, oPath, overwrite=True):
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
        # Load JSON ----------------------------------------------------------
        with open(fName, 'r') as file:
            try:
                data = json.load(file)
            except:
                print("Corrupted json file! Skipping {}".format(file))
                pass
        # Process battles in file --------------------------------------------
        histSize = len(data)
        if histSize > 1:
            # Older s3s versions ---------------------------------------------
            for i in range(histSize):
                try:
                    bDetail = data[i]['data']['vsHistoryDetail']
                    # Process battle history ---------------------------------
                    battle = bat.Battle(bDetail)
                    # Export battle history ----------------------------------
                    bPath = battle.dumpBattle(oPath, overwrite=overwrite)
                    bPaths.append(bPath)
                except:
                    pass
        else:
            # New s3s versions (> 1.3.4) -------------------------------------
            try:
                bDetail = data['data']['vsHistoryDetail']
                # Process battle history -------------------------------------
                battle = bat.Battle(bDetail)
                # Export battle history --------------------------------------
                bPath = battle.dumpBattle(oPath, overwrite=overwrite)
                bPaths.append(bPath)
            except:
                pass
    return bPaths

###########################################################################
# Get filepaths
###########################################################################
def getDataFilepaths(
        iPath, fldrPat='export-*', 
        filePat='results.json',
        newPat=True
    ):
    """Gets the filepaths in which files with a certain pattern can be found inside folders with a given pattern.

    Args:
        iPath (str): Base path in which we will perform the folders search.
        fldrPat (str, optional): Glob pattern for folder matches. Defaults to 'export-\*'.
        filePat (str, optional): Glob pattern for file matches inside the folders. Defaults to 'results.json'.
        newPat (bool, optional): Set to True if using s3s >=v1.3.4
        
    Returns:
        list: List of filepaths that match the provided patterns.
    """    
    hFolders = aux.getHistoryFolders(iPath, fldrPat=fldrPat)
    hFiles = aux.getHistoryFiles(hFolders, pattern=filePat)
    if newPat:
        fnames = glob(path.join(iPath, 'exports/results/*.json'))
        hFiles.extend(fnames)
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

