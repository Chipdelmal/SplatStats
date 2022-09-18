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

i = 1
bDetail = data[i]['data']['vsHistoryDetail']
battle = bat.Battle(bDetail)
battle.enemyTeams[0]

bDetail.keys()
bDetail['festMatch']
bDetail['vsRule']
bDetail['vsMode']
bDetail['myTeam']['players'][0]['result']
bDetail['otherTeams'][0]['players'][0]['result']

###############################################################################
# Battle Info
###############################################################################

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
players = bDetail['myTeam']['players']
playersInfo = par.getPlayersBattleInfo(players)
###############################################################################
# Enemy Info
###############################################################################
oTeam = bDetail['otherTeams'][0]
oPlayers = oTeam['players']
enemiesInfo = par.getPlayersBattleInfo(oPlayers)




# pix = 2
# player = players[pix]
# # Condensed Info ----------------------------------------------------------
# resultsDict = par.getPlayerResults(player)
# weaponsDict = par.getPlayerWeapon(player)
# gearDict = par.getGear(player)
# # Dictionary --------------------------------------------------------------
# pDict = {
#     'player name': player['name'], 'player name id': player['nameId'], 
#     **weaponsDict,
#     **resultsDict, 'paint': player['paint'],
#     **gearDict,
#     'self': player['isMyself'],
#     'player id': player['id']
# }
# playersInfo[pix] = pDict

