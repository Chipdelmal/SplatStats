#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        # Parse players' battles dataframes -----------------------------------
        self.players = {
            name: Player(name, bPaths, timezone=timezone)
            for name in names
        }