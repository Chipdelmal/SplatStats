#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from collections import Counter
from sklearn.feature_extraction import DictVectorizer

def calculateDominanceMatrixWins(statInkBattles):
    # Get the weapons dictionaries for each team ------------------------------
    btls = statInkBattles
    (alpha, bravo) = (
        btls[[f'A{i}-weapon' for i in range(1, 5)]],
        btls[[f'B{i}-weapon' for i in range(1, 5)]]
    )
    winrs = list(btls['win'])
    # Vectorize (encode) the weapons used by each team in the battles ---------
    vct = DictVectorizer(sparse=False)
    wpnsDA = [dict(Counter(alpha.iloc[i])) for i in range(alpha.shape[0])]
    wpnsDB = [dict(Counter(bravo.iloc[i])) for i in range(bravo.shape[0])]
    (wpnsVA, wpnsVB) = (vct.fit_transform(wpnsDA), vct.fit_transform(wpnsDA))
    wpnsNames = list(vct.get_feature_names_out())
    # Assemble matrix ---------------------------------------------------------
    domMtx = np.zeros((len(wpnsNames), len(wpnsNames)))
    for ix in range(len(winrs)):
        (bAWpns, bBWpns, winTeam) = (wpnsDA[ix], wpnsDB[ix], winrs[ix])
        (bAVctr, bBVctr) = (wpnsVA[ix], wpnsVB[ix])
        if winTeam:
            rxs = [wpnsNames.index(wpn) for wpn in bBWpns]
            for rx in rxs:
                domMtx[rx] = domMtx[rx]+bAVctr
        else:
            rxs = [wpnsNames.index(wpn) for wpn in bAWpns]
            for rx in rxs:
                domMtx[rx] = domMtx[rx]+bBVctr
    # Transpose and return ----------------------------------------------------
    domMtx = domMtx.T  
    return (wpnsNames, domMtx)