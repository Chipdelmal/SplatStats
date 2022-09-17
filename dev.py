import json

###############################################################################
# Results Files
###############################################################################
fName = '/home/chipdelmal/Documents/GitHub/s3s/export-1663442390/results.json'
with open(fName, 'r') as file:
    data = json.load(file)
histSize = len(data)

i = 25
battleHist = data[i]['data']

bDetail = battleHist['vsHistoryDetail']
bKeys = bDetail.keys()

kNames = ('id', 'vsRule', 'vsMode', 'result')
(bId, vRule, vMode, result) = [bDetail.get(k) for k in kNames]