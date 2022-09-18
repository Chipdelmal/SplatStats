import json
import parsers as par

###############################################################################
# Load File
###############################################################################
fName = '/home/chipdelmal/Documents/GitHub/s3s/export-1663442390/results.json'
with open(fName, 'r') as file:
    data = json.load(file)
histSize = len(data)

i = 20
battleHist = data[i]['data']
bDetail = battleHist['vsHistoryDetail']
###############################################################################
# Battle Info
###############################################################################
bKeys = bDetail.keys()
kNames = (
    'id', 'vsRule', 'vsMode', 'judgement', 'awards', 'duration', 'knockout',
    'playedTime'
)
(bId, vRule, vMode, result, awards, duration, knock, date) = [
    bDetail.get(k) for k in kNames
]
###############################################################################
# Team Info
###############################################################################
team = bDetail['myTeam']
###############################################################################
# Players Info
###############################################################################
players = bDetail['myTeam']['players']

pix = 2
player = players[pix]
# Condensed Info --------------------------------------------------------------
resultsDict = par.getPlayerResults(player)
weaponsDict = par.getPlayerWeapon(player)
gearDict = par.getGear(player)
# Dictionary ------------------------------------------------------------------
pDict = {
    'player name': player['name'], 'player name id': player['nameId'], 
    **weaponsDict,
    **resultsDict, 'paint': player['paint'],
    **gearDict,
    'self': player['isMyself'],
    'player id': player['id']
}
pDict

