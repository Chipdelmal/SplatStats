import json
import parsers as par
import Battle as bat
import pandas as pd

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
battle.id

bDetail.keys()
bDetail['festMatch']

