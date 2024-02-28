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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


plyrName = 'čħîþ ウナギ'
(iPath, bPath, oPath) = (
    path.expanduser('~/Documents/BattlesDocker/jsons'),
    path.expanduser('~/Documents/BattlesDocker/battles'),
    path.expanduser('~/Documents/BattlesDocker/out')
)
fontPath = '/home/chipdelmal/Documents/GitHub/SplatStats/other/'
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=True)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Team Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
(plyrHist, btleHist) = (plyr.battlesHistory, plyr.battleRecords)
###############################################################################
# Battles Analysis
###############################################################################
matchType = 'Turf War'
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
    XE, y, test_size=0.15
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
###############################################################################
# Frequency Analysis
###############################################################################
ix = 0
matchType = 'Clam Blitz'
(wpA, wpE) = ({'W': [], 'L': []}, {'W': [], 'L': []})
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
        if btlResult:
            wpA['W'].extend(list(dfAlly['main weapon']))
            wpE['W'].extend(list(dfEnmy['main weapon']))
        else:
            wpA['L'].extend(list(dfAlly['main weapon']))
            wpE['L'].extend(list(dfEnmy['main weapon']))

norm = True
ran = 20
probe = Counter(wpA['W']).most_common()
(x, y) = (
    [i[0] for i in probe][:ran][::-1],
    [i[1] for i in probe][:ran][::-1]
)
if norm:
    tMatch = np.sum(y)
    y = [i/tMatch for i in y]
splat.polarBarChart(
    x, y,
    rRange=(0, 270),
    yRange=(0, .5),
    ticksFmt={
        'lw': 1, 'range': (-0.5, -0.25), 
        'color': '#000000DD', 'fontsize': 8, 'fmt': '{:.2f}'
    }
)

def getWeaponClass(weapon, wpnClassDict=splat.WPN_CLASS):
    dictKey = filter(lambda x: (weapon in wpnClassDict[x]), wpnClassDict)
    if len(dictKey)==0:
        return None
    else:
        return dictKey[0]