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
    wBool = False
    if winString=='WIN':
        wBool = True
    return wBool