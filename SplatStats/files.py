
import json
import warnings
from os import path
import pandas as pd
from glob import glob
from termcolor import colored
from dateutil.parser import parse
import SplatStats.constants as cst
import SplatStats.auxiliary as aux
import SplatStats.Battle as bat
warnings.simplefilter(action='ignore', category=FutureWarning)

###########################################################################
# Dump all battles
###########################################################################
def dumpBattlesFromJSONS(historyFilepaths, oPath):
    hFiles = historyFilepaths
    fNum = len(hFiles)
    bPaths = []
    for (ix, fName) in enumerate(hFiles):
        # Print progress --------------------------------------------------
        cpt = colored(f'* Parsing JSONs {ix+1:05d}/{fNum:05d}', 'red')
        print(cpt, end='\r')
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
def getBattleFilepaths(bPath, filePat='*.pkl'):
    battleFilepaths = glob(path.join(bPath, filePat))
    return battleFilepaths
    
def getDataFilepaths(iPath, fldrPat='export-*', filePat='results.json'):
    hFolders = aux.getHistoryFolders(iPath, fldrPat=fldrPat)
    hFiles = aux.getHistoryFiles(hFolders, pattern=filePat) 
    return hFiles

###########################################################################
# Get player history dataframe
###########################################################################
# def getPlayerHistory(self, playerName, category='player name'):
#     fNum = len(self.battleFilepaths)
#     playerDFs = []
#     for (ix, batFile) in enumerate(self.battleFilepaths):
#         # Print progress --------------------------------------------------
#         cpt = colored(f'* Loading History {ix+1:05d}/{fNum:05d}', 'red')
#         print(cpt, end='\r')
#         # Process battle --------------------------------------------------
#         battle = aux.loadBattle(batFile)
#         rowA = battle.getAllyByCategory(playerName, category=category)
#         rowE = battle.getEnemyByCategory(playerName, category=category)
#         # Append row to list ----------------------------------------------
#         if rowA is not None:
#             playerDFs.append(rowA)
#         if rowE is not None:
#             playerDFs.append(rowE)
#     playerDF = pd.concat(playerDFs, axis=0)
#     playerDF.astype(cst.BATTLE_DTYPES)
#     # Re-arrange dataframe ------------------------------------------------
#     playerDF.sort_values(by='datetime', inplace=True)
#     playerDF.reset_index(drop=True, inplace=True)
#     playerDF.drop([
#         'player name', 'player name id', 'self'
#     ], axis=1, inplace=True)
#     playerDF.drop_duplicates(inplace=True)
#     return  playerDF
