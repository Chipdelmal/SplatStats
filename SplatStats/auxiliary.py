#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl
from os import path
from glob import glob

def gearPrepend(gearType):
    if (gearType=='headGear'):
        gPrep = 'head'
    elif (gearType=='clothingGear'):
        gPrep = 'shirt'
    elif (gearType=='shoesGear'):
        gPrep = 'shoes'
    return gPrep

def boolWinLose(winString):
    if winString=='WIN':
        wBool = 'W'
    elif winString == 'LOSE':
        wBool = 'L'
    else:
        wBool = 'NA'
    return wBool

def boolKO(koString):
    if (koString == 'WIN') or (koString == 'LOSE'):
        koBool = True
    else:
        koBool = False
    return koBool

def datetimeToString(datetime):
    return datetime.strftime("%Y_%m_%d-%Hh%M")

def loadBattle(fPath):
    with open(fPath, 'rb') as f:
        battle = pkl.load(f)
    return battle

def getHistoryFolders(histPath, fldrPat='export-*'):
    histFolders = glob(path.join(histPath, fldrPat))
    return histFolders

def getHistoryFiles(histFolders, pattern='results.json'):
    histFiles = []
    for f in histFolders:
        histFiles.extend(glob(path.join(f, pattern)))
    return histFiles

def awardsToStrings(awardsDF, sep='@'):
    awds = []
    for i in range(awardsDF.shape[0]):
        row = awardsDF.iloc[i]
        awds.append(f"{row['name']}{sep}{row['rank']}{sep}{row['place']}")
    return awds
    
flattenList = lambda irregular_list:[element for item in irregular_list for element in flattenList(item)] if type(irregular_list) is list else [irregular_list]

def isNotebook():
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
