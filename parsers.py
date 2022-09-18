#!/usr/bin/env python
# -*- coding: utf-8 -*-

import auxiliary as aux

def getPlayerWeapon(player):
    pWeapon = player['weapon']
    wDict = {
        'main weapon': pWeapon['name'], 
        'sub weapon': pWeapon['subWeapon']['name'], 
        'special weapon': pWeapon['specialWeapon']['name']
    }
    return wDict

def getPlayerResults(player):
    pResult = player['result']
    pResults = {
        k: pResult[k] for k in ('kill', 'death', 'assist', 'special')
    }
    return pResults

def getGearUnit(player, gType='headGear'):
    gear = player[gType]
    gPrep = aux.gearPrepend(gType)
    keyPat = [f'{gPrep} {s}' for s in ['name', 'main', 'sub_0', 'sub_1', 'sub_2']]
    adPow = dict.fromkeys(keyPat)
    adPow[f'{gPrep} name'] = gear['name']
    adPow[f'{gPrep} main'] = gear['primaryGearPower']['name']
    for (i, g) in enumerate(gear['additionalGearPowers']):
        adPow[f'{gPrep} sub_{i}'] = g['name']
    return adPow

def getGear(player):
    gearTypes = ('headGear', 'clothingGear', 'shoesGear')
    (headDict, clothesDict, shoesDict) = [
        getGearUnit(player, gType) for gType in gearTypes
    ]
    return {**headDict, **clothesDict, **shoesDict}

def getPlayersBattleInfo(players):
    playersInfo = [None]*len(players)
    for (pix, player) in enumerate(players):
        # Condensed Info ----------------------------------------------------------
        resultsDict = getPlayerResults(player)
        weaponsDict = getPlayerWeapon(player)
        gearDict = getGear(player)
        # Dictionary --------------------------------------------------------------
        pDict = {
            'player name': player['name'], 'player name id': player['nameId'], 
            **weaponsDict,
            **resultsDict, 'paint': player['paint'],
            **gearDict,
            'self': player['isMyself']
            # 'player id': player['id']
        }
        playersInfo[pix] = pDict
    return playersInfo