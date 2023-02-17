
import json

# with open('./InkStat/weapon.json', 'r') as f:
#   WEAPONS = json.load(f)
# wpnKeys = [i['key'] for i in WEAPONS]


LOBBY_MODE = {
  'regular': 'Regular',
  'bankara_challenge': 'Anarchy (Series)',
  'bankara_open': 'Anarchy (Open)',
  'xmatch': 'X Battle',
  'splatfest_challenge': 'Splatfest (Pro)',
  'splatfest_open': 'Splatfest (Open)'
}
GAME_MODE = {
  'nawabari': 'Turf War',
  'area': 'Splat Zones',
  'yagura': 'Tower Control',
  'hoko': 'Rainmaker',
  'asari': 'Clam Blitz'
}
STATINK_DTYPES = {
  # Match information -------------------------------------------------------
  '# season': 'string',
  #'period': 'datetime64'
  'game-ver': 'string',
  'lobby': 'string',
  'mode': 'string',
  'stage': 'string',
  'time': 'uint16',
  'win': 'string',
  'knockout': 'string',
  'rank': 'string',
  'power': 'float',
  # Team results ------------------------------------------------------------
  'alpha-inked': 'Int64',         'bravo-inked': 'Int64',
  'alpha-ink-percent': 'float',   'bravo-ink-percent': 'float',
  'alpha-count': 'Int64',         'bravo-count': 'Int64',
  'alpha-color': 'string',        'bravo-color': 'string',
  'alpha-theme': 'string',        'bravo-theme': 'string',
  # Team A stats ------------------------------------------------------------
  'A1-weapon': 'string',   'A1-kill-assist': 'Int8',
  'A1-kill': 'Int8',       'A1-assist': 'Int8', 
  'A1-death': 'Int8',      'A1-special': 'Int8',
  'A1-inked': 'Int16',     'A1-abilities': 'object',
  'A2-weapon': 'string',   'A2-kill-assist': 'Int8',
  'A2-kill': 'Int8',       'A2-assist': 'Int8', 
  'A2-death': 'Int8',      'A2-special': 'Int8',
  'A2-inked': 'Int16',     'A2-abilities': 'object',
  'A3-weapon': 'string',   'A3-kill-assist': 'Int8',
  'A3-kill': 'Int8',       'A3-assist': 'Int8', 
  'A3-death': 'Int8',      'A3-special': 'Int8',
  'A3-inked': 'Int16',     'A3-abilities': 'object',
  'A4-weapon': 'string',   'A4-kill-assist': 'Int8',
  'A4-kill': 'Int8',       'A4-assist': 'Int8', 
  'A4-death': 'Int8',      'A4-special': 'Int8',
  'A4-inked': 'Int16',     'A4-abilities': 'object',
  # Team B stats ------------------------------------------------------------
  'B1-weapon': 'string',   'B1-kill-assist': 'Int8',
  'B1-kill': 'Int8',       'B1-assist': 'Int8', 
  'B1-death': 'Int8',      'B1-special': 'Int8',
  'B1-inked': 'Int16',     'B1-abilities': 'object',
  'B2-weapon': 'string',   'B2-kill-assist': 'Int8',
  'B2-kill': 'Int8',       'B2-assist': 'Int8', 
  'B2-death': 'Int8',      'B2-special': 'Int8',
  'B2-inked': 'Int16',     'B2-abilities': 'object',
  'B3-weapon': 'string',   'B3-kill-assist': 'Int8',
  'B3-kill': 'Int8',       'B3-assist': 'Int8', 
  'B3-death': 'Int8',      'B3-special': 'Int8',
  'B3-inked': 'Int16',     'B3-abilities': 'object',
  'B4-weapon': 'string',   'B4-kill-assist': 'Int8',
  'B4-kill': 'Int8',       'B4-assist': 'Int8', 
  'B4-death': 'Int8',      'B4-special': 'Int8',
  'B4-inked': 'Int16',     'A4-abilities': 'object',
  # Medals ------------------------------------------------------------------
  'medal1-name': 'string', 'medal1-grade': 'string',
  'medal2-name': 'string', 'medal2-grade': 'string',
  'medal3-name': 'string', 'medal3-grade': 'string'    
}