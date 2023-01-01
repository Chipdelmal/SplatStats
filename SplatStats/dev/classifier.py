#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sys import argv
from os import path
from collections import Counter
import SplatStats as splat
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, DictVectorize
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


plyrName = 'čħîþ ウナギ'
(iPath, bPath, oPath) = (
    path.expanduser('~/Documents/Sync/BattlesDocker/jsons'),
    path.expanduser('~/Documents/Sync/BattlesDocker/battles'),
    path.expanduser('~/Documents/Sync/BattlesDocker/out')
)
fontPath = '/home/chipdelmal/Documents/GitHub/SplatStats/other/'
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=False)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Team Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
###############################################################################
# Battles Analysis
###############################################################################
btleHist = plyr.battleRecords
matchType = 'All'
(vectA, vectE) = (
    DictVectorizer(sparse=False), DictVectorizer(sparse=False)
)
###############################################################################
# Assemble ML I/O
#   https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
#   https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html#sklearn.feature_extraction.text.HashingVectorizer
###############################################################################
ix = 0
(wpA, wpE, out) = ([], [], [])
for ix in range(len(btleHist)):
    # Get battle entry --------------------------------------------------------
    btl = btleHist[ix]
    if (btl.matchType==matchType) or (matchType=='All'):
        # Get teams dataframes and result -------------------------------------
        (dfAlly, dfEnmy) = (btl.alliedTeam, pd.concat(btl.enemyTeams))
        (btlResult, btlKO) = (
            (1 if btl.alliedTeam['win'].iloc[0]!='L' else 0),
            btl.ko
        )
        # Teams weapons -------------------------------------------------------
        (wpAlly, wpEnmy) = [
            dict(Counter(i['main weapon'])) for i in (dfAlly, dfEnmy)
        ]
        wpA.append(wpAlly)
        wpE.append(wpEnmy)
        # Battle outcome ------------------------------------------------------
        koMult = (1 if btlKO else 1)
        result = koMult*btlResult
        out.append(result)
###############################################################################
# Transform I/O
###############################################################################
y = out
XE = vectE.fit_transform(wpE)
wpLabels = vectE.get_feature_names_out()
###############################################################################
# Train
###############################################################################
(X_train, X_test, y_train, y_test) = train_test_split(
    XE, y, test_size=0.1
)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
# Evaluate --------------------------------------------------------------------
prediction = clf.predict(X_test)
print(accuracy_score(prediction, y_test))
print(confusion_matrix(prediction, y_test))
print(classification_report(prediction, y_test))
###############################################################################
# Evaluate
###############################################################################
probe = {
    'Splattershot Jr.': 2,
    'Splattershot': 2
}
xi = vectE.transform([probe])
clf.predict(xi)