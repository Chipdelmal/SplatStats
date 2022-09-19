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
        
    Methods
    -------
    """
    ###########################################################################
    # Player info
    ###########################################################################
    def __init__(self, battle):
        return True