#!/usr/bin/env python
# -*- coding: utf-8 -*-

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