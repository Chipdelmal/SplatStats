#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from SplatStats.Player import Player

class Team:
    ###########################################################################
    # Team init
    ###########################################################################
    def __init__(self, names, bPaths, ids=None, timezone=None):
        self.names = names
        self.ids = ids
        self.bPaths = bPaths
        self.timezone = timezone
        # Generate player objects ---------------------------------------------
        if (type(bPaths[0]) is type('dummy')):
            self.players = {
                name: Player(name, bPaths, timezone=timezone)
                for name in names
            }
        else:
            self.players = {
                name: Player(name, bPth, timezone=timezone)
                for (bPth, name) in zip(bPaths, names)
            }
        # Assemble battle team dataframe --------------------------------------
        self.battleHistory = self.assembleTeamHistoryFromBattles()
    ###########################################################################
    # Assemble team battle dataframe
    ###########################################################################
    def assembleTeamHistoryFromBattles(self):
        dfs = []
        for nme in self.names:
            dfTemp = self.players[nme].battlesHistory
            dfTemp['player'] = [nme]*(dfTemp.shape[0])
            dfTemp['matches'] = [1]*(dfTemp.shape[0])
            dfs.append(dfTemp)
        dfTeam = pd.concat(dfs, axis=0)
        return dfTeam
    ###########################################################################
    # Reshape team battle dataframe by period
    ###########################################################################
    def reshapeTeamHistoryByPeriod(
            self, 
            cats=['kill', 'death', 'assist', 'special', 'paint', 'matches'],
            period='H'
        ):
        catsDF = ['player', 'datetime'] + cats
        dfGrp = self.battleHistory[catsDF].groupby(['datetime', 'player']).sum()
        dfPadded = dfGrp.unstack(fill_value=0).stack()
        # Generate series
        dfByHour = dfPadded.unstack().resample(period).sum().stack()
        return dfByHour