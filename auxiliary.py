#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dill as pkl

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