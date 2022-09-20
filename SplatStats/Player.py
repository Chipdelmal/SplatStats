#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl
from os import path
from dateutil.parser import parse
import SplatStats.parsers as par
import SplatStats.auxiliary as aux
import SplatStats.Battle as bat
import SplatStats.History as hst

class Player:
    """
    Attributes
    ----------
    name : str
        Player's in-game name
    id : int
        Player's in-game id
        
    Methods
    -------
    """
    ###########################################################################
    # Player info
    ###########################################################################
    def __init__(self, name, id=0):
        self.name = name
        self.id = id
        return True