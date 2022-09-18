#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import Battle as bat
import auxiliary as aux

###############################################################################
# Load File
###############################################################################
fName = '/home/chipdelmal/Documents/GitHub/s3s/export-1663442390/results.json'
# fName = '/home/chipdelmal/Documents/GitHub/s3s/export-1663524543/results.json'
with open(fName, 'r') as file:
    data = json.load(file)
histSize = len(data)
###############################################################################
# Explore operations
###############################################################################
i = 2
bDetail = data[i]['data']['vsHistoryDetail']
# Process battle history ------------------------------------------------------
battle = bat.Battle(bDetail)
# Export battle history -------------------------------------------------------
battle.dumpBattle('./Battles/')
# Import battle history -------------------------------------------------------
fName = aux.datetimeToString(battle.datetime)
battleLoaded = aux.loadBattle(f'./Battles/{fName}.pkl')

