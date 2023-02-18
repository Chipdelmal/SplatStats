
# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

import re
from os import path
from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from collections import Counter
import SplatStats as splat

DATA_PATH = '/Users/sanchez.hmsc/Documents/SyncMega/BattlesDocker/battle-results-csv'
FPATHS = glob(path.join(DATA_PATH, '*-*-*.csv'))

###############################################################################
# Read Full Data
###############################################################################
DFS_LIST = [pd.read_csv(f, dtype=splat.STATINK_DTYPES, parse_dates=['period']) for f in FPATHS]
FULL_DF = pd.concat(DFS_LIST)
cols = [i.replace('#', '').strip() for i in list(FULL_DF.columns)]
df = FULL_DF.copy()
###############################################################################
# Make Replacements
###############################################################################
statInk = splat.StatInk(DATA_PATH)
btls = statInk.battlesResults

###############################################################################
# Aggregate by date
###############################################################################
df['dummy'] = [1]*df.shape[0]
counts = df.groupby([df['period'].dt.date]).count()['dummy']
(fig, ax) = (plt.figure(), plt.axes())
ax.plot(list(counts))
df['mode'] = [splat.GAME_MODE[lob] for lob in df['mode']]



# ###############################################################################
# # Testing class
# ###############################################################################
# 
# knocks = [i for i in statInk.battlesResults['knockout'] if (i>=0)]

# btls = statInk.battlesResults
# alpha = btls[[f'A{i}-weapon' for i in range(1, 5)]]
# winrs = btls['win']
# bravo = btls[[f'B{i}-weapon' for i in range(1, 5)]]

# (vectA, vectB) = [DictVectorizer(sparse=False) for _ in range(2)]
# bA = [dict(Counter(alpha.iloc[i])) for i in range(alpha.shape[0])]
# dA = vectB.fit_transform(bA)
# bB = [dict(Counter(bravo.iloc[i])) for i in range(bravo.shape[0])]
# dB = vectB.fit_transform(bB)

# labels = list(btls['win'])
# ###############################################################################
# # Train
# ###############################################################################
# (X_train, X_test, y_train, y_test) = train_test_split(
#     dB, labels, test_size=0.3
# )
# clf = RandomForestClassifier()
# clf.fit(X_train, y_train)
# # Evaluate --------------------------------------------------------------------
# prediction = clf.predict(X_test)
# print(accuracy_score(prediction, y_test))
# print(confusion_matrix(prediction, y_test))
# print(classification_report(prediction, y_test))