#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from glob import glob
import pandas as pd
import SplatStats.statInkConstants as ink

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
    def __init__(
            self, resultsPaths, 
            fNamePattern='*-*-*.csv'
        ):
        self.fPaths = glob(path.join(resultsPaths, fNamePattern))
        # Read csv's into a dataframe ----------------------------------------
        rawDFList = [
            pd.read_csv(
                f, 
                parse_dates=['period'], 
                dtype=ink.STATINK_DTYPES, 
                on_bad_lines='warn'
            ) for f in self.fPaths
        ]
        self.rawResults = pd.concat(rawDFList)
        # Clean dataframe to standard names/times ----------------------------
        self.battlesResults = self.cleanBattlesDataframe(self.rawResults)
        
    def cleanBattlesDataframe(
            self, rawResults,
            naColor='#00000000', naBool=-1, naString='NA', 
            naInt=0, ammendWeapons=True
        ):
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
        # Ammend Duplicate Weapons (US standard) -----------------------------
        if ammendWeapons:
            for wpnTuple in ink.WPNS_REPLICAS:
                df.replace(wpnTuple[0], wpnTuple[1], inplace=True)
        # Replace knockouts, ranks and wins ----------------------------------
        df['knockout'] = [int(k) if (type(k) is bool) else naBool for k in df['knockout']]
        df['rank'] = [r if type(r) is str else naString for r in df['rank']]
        df['power'] = df['power'].fillna(naInt)
        df['win'] = [True if (i=='alpha') else False for i in df['win']]
        # Cleanup colors -----------------------------------------------------
        df['alpha-color'] = [f'#{c}' if type(c) is str else naColor for c in df['alpha-color']]
        df['bravo-color'] = [f'#{c}' if type(c) is str else naColor for c in df['bravo-color']]
        # Coherce into data types and return dataframe -----------------------
        df.astype(ink.SPLATSTATS_DTYPES, copy=False)
        return df
    
