
import json

with open('./InkStat/weapon.json', 'r') as f:
  WEAPONS = json.load(f)
wpnKeys = [i['key'] for i in WEAPONS]


GAME_MODE = {
    'nawabari': 'Turf War',
    'area': 'Splat Zones',
    'yagura': 'Tower Control',
    'hoko': 'Rainmaker',
    'asari': 'Clam Blitz'
}

LOBBY_MODE = {
    'regular': 'Regular',
    'bankara_challenge': 'Anarchy (Series)',
    'bankara_open': 'Anarchy (Open)',
    'xmatch': 'X Battle',
    'splatfest_challenge': 'Splatfest (Pro)',
    'splatfest_open': 'Splatfest (Open)'
}