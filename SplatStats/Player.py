#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl
from os import path
from dateutil.parser import parse
import SplatStats.Battle as bat
import SplatStats.parsers as par
import SplatStats.auxiliary as aux

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
    def __init__(self, name, id):
        self.name = name
        self.id = id
        return True