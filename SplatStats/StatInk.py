#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from glob import glob
import pandas as pd
import SplatStats.constantsStatInk as ink
import SplatStats.parsers as par

class StatInk:
    """
    Attributes
    ----------
    fPaths: list of paths
        Filepaths of the battle results csv files loaded for analysis
    rawResults: dataframe
        Dataframe containing battle results information directly from stat.ink
    battleResults: dataframe
        Clean dataframe containing results in human-readable form
    """
    def __init__(self, resultsPaths, fNamePattern='*-*-*.csv'):
        self.fPaths = glob(path.join(resultsPaths, fNamePattern))
        # Read csv's into a dataframe ----------------------------------------
        rawDFList = [
            pd.read_csv(
                f, parse_dates=['period'], # dtype=dTypes, 
            ) for f in self.fPaths
        ]
        self.rawResults = pd.concat(rawDFList)
        # Clean dataframe to standard names/times ----------------------------
        self.battlesResults = self.cleanBattlesDataframe(self.rawResults)
        
    def cleanBattlesDataframe(self, rawResults):
        df = rawResults.copy()
        # Cleaning column names ----------------------------------------------
        df.columns = [i.replace('#', '').strip() for i in list(rawResults.columns)]
        # Replace simple columns ---------------------------------------------
        df['lobby'] = [ink.LOBBY_MODE[l] for l in df['lobby']]
        df['mode']  = [ink.GAME_MODE[m] for m in df['mode']]
        df['stage'] = [ink.STGS_DICT[s] for s in df['stage']]
        # Replace weapon names (US standard) ---------------------------------
        for i in range(1, 5):
            df[f'A{i}-weapon'] = [ink.WPNS_DICT[w] for w in df[f'A{i}-weapon']]
            df[f'B{i}-weapon'] = [ink.WPNS_DICT[w] for w in df[f'B{i}-weapon']]
        # Replace knockouts and wins -----------------------------------------
        df['knockout'] = [par.boolToInt(k) for k in df['knockout']]
        # Cleanup colors -----------------------------------------------------
        nullColor = '#00000000'
        df['alpha-color'] = [f'#{c}' if type(c) is str else nullColor for c in df['alpha-color']]
        df['bravo-color'] = [f'#{c}' if type(c) is str else nullColor for c in df['bravo-color']]
        # Return standard dataframe ------------------------------------------
        return df