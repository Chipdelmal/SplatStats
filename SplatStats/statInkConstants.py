
import numpy as np

###############################################################################
# Schemas from:
#   https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
###############################################################################
# import json
# with open('./InkStat/weapon.json', 'r') as f:
#   WEAPONS = json.load(f)
# wpnKeys = [i['key'] for i in WEAPONS]
# wpnDict = {
#   wpnKeys[ix]: WEAPONS[ix]['name']['en_US'] for ix in range(len(wpnKeys))
# }

GAME_MODE = {
  'nawabari': 'Turf War', 'area': 'Splat Zones', 
  'yagura': 'Tower Control', 'hoko': 'Rainmaker', 
  'asari': 'Clam Blitz'
}

LOBBY_MODE = {
  'regular': 'Regular',
  'bankara_challenge': 'Anarchy (Series)',
  'bankara_open': 'Anarchy (Open)',
  'xmatch': 'X Battle',
  'splatfest_challenge': 'Splatfest (Pro)',
  'splatfest_open': 'Splatfest (Open)',
  'event': 'Event'
}

WPNS_DICT = {
  '52gal': '.52 Gal',
  '96gal': '.96 Gal',
  '96gal_deco': '.96 Gal Deco',
  'bold': 'Sploosh-o-matic',
  'bold_neo': 'Neo Sploosh-o-matic',
  'bottlegeyser': 'Squeezer',
  'heroshooter_replica': 'Hero Shot Replica',
  'jetsweeper': 'Jet Squelcher',
  'jetsweeper_custom': 'Custom Jet Squelcher',
  'momiji': 'Custom Splattershot Jr.',
  'nzap85': "N-ZAP '85",
  'nzap89': "N-ZAP '89",
  'prime': 'Splattershot Pro',
  'prime_collabo': 'Forge Splattershot Pro',
  'promodeler_mg': 'Aerospray MG',
  'promodeler_rg': 'Aerospray RG',
  'sharp': 'Splash-o-matic',
  'sharp_neo': 'Neo Splash-o-matic',
  'spaceshooter': 'Splattershot Nova',
  'spaceshooter_collabo': 'Annaki Splattershot Nova',
  'sshooter': 'Splattershot',
  'sshooter_collabo': 'Tentatek Splattershot',
  'wakaba': 'Splattershot Jr.',
  'clashblaster': 'Clash Blaster',
  'clashblaster_neo': 'Clash Blaster Neo',
  'hotblaster': 'Blaster',
  'longblaster': 'Range Blaster',
  'nova': 'Luna Blaster',
  'nova_neo': 'Luna Blaster Neo',
  'rapid': 'Rapid Blaster',
  'rapid_deco': 'Rapid Blaster Deco',
  'rapid_elite': 'Rapid Blaster Pro',
  'rapid_elite_deco': 'Rapid Blaster Pro Deco',
  'sblast92': "S-BLAST '92",
  'h3reelgun': 'H-3 Nozzlenose',
  'h3reelgun_d': 'H-3 Nozzlenose D',
  'l3reelgun': 'L-3 Nozzlenose',
  'l3reelgun_d': 'L-3 Nozzlenose D',
  'dualsweeper': 'Dualie Squelchers',
  'dualsweeper_custom': 'Custom Dualie Squelchers',
  'kelvin525': 'Glooga Dualies',
  'maneuver': 'Splat Dualies',
  'quadhopper_black': 'Dark Tetra Dualies',
  'quadhopper_white': 'Light Tetra Dualies',
  'sputtery': 'Dapple Dualies',
  'sputtery_hue': 'Dapple Dualies Nouveau',
  'carbon': 'Carbon Roller',
  'carbon_deco': 'Carbon Roller Deco',
  'dynamo': 'Dynamo Roller',
  'dynamo_tesla': 'Gold Dynamo Roller',
  'splatroller': 'Splat Roller',
  'splatroller_collabo': 'Krak-On Splat Roller',
  'variableroller': 'Flingza Roller',
  'wideroller': 'Big Swig Roller',
  'wideroller_collabo': 'Big Swig Roller Express',
  'fincent': 'Painbrush',
  'hokusai': 'Octobrush',
  'hokusai_hue': 'Octobrush Nouveau',
  'pablo': 'Inkbrush',
  'pablo_hue': 'Inkbrush Nouveau',
  'drivewiper': 'Splatana Wiper',
  'drivewiper_deco': 'Splatana Wiper Deco',
  'jimuwiper': 'Splatana Stamper',
  'bamboo14mk1': 'Bamboozler 14 Mk I',
  'liter4k': 'E-liter 4K',
  'liter4k_scope': 'E-liter 4K Scope',
  'rpen_5h': 'Snipewriter 5H',
  'soytuber': 'Goo Tuber',
  'soytuber_custom': 'Custom Goo Tuber',
  'splatcharger': 'Splat Charger',
  'splatcharger_collabo': 'Z+F Splat Charger',
  'splatscope': 'Splatterscope',
  'splatscope_collabo': 'Z+F Splatterscope',
  'squiclean_a': 'Classic Squiffer',
  'bucketslosher': 'Slosher',
  'bucketslosher_deco': 'Slosher Deco',
  'explosher': 'Explosher',
  'furo': 'Bloblobber',
  'furo_deco': 'Bloblobber Deco',
  'hissen': 'Tri-Slosher',
  'hissen_hue': 'Tri-Slosher Nouveau',
  'moprin': 'Dread Wringer',
  'screwslosher': 'Sloshing Machine',
  'screwslosher_neo': 'Sloshing Machine Neo',
  'barrelspinner': 'Heavy Splatling',
  'barrelspinner_deco': 'Heavy Splatling Deco',
  'examiner': 'Heavy Edit Splatling',
  'hydra': 'Hydra Splatling',
  'kugelschreiber': 'Ballpoint Splatling',
  'kugelschreiber_hue': 'Ballpoint Splatling Nouveau',
  'nautilus47': 'Nautilus 47',
  'splatspinner': 'Mini Splatling',
  'splatspinner_collabo': 'Zink Mini Splatling',
  'campingshelter': 'Tenta Brella',
  'campingshelter_sorella': 'Tenta Sorella Brella',
  'parashelter': 'Splat Brella',
  'parashelter_sorella': 'Sorella Brella',
  'spygadget': 'Undercover Brella',
  'lact450': 'REEF-LUX 450',
  'tristringer': 'Tri-Stringer',
  'tristringer_collabo': 'Inkline Tri-Stringer'
}

STGS_DICT = {
  'yunohana': 'Scorch Gorge', 'gonzui': 'Eeltail Alley',
  'kinmedai': "Museum d'Alfonsino", 'mategai': 'Undertow Spillway',
  'namero': 'Mincemeat Metalworks', 'yagara': 'Hagglefish Market',
  'masaba': 'Hammerhead Bridge', 'mahimahi': 'Mahi-Mahi Resort',
  'zatou': 'MakoMart', 'chozame': 'Sturgeon Shipyard',
  'amabi': 'Inkblot Art Academy', 'sumeshi': 'Wahoo World',
  'hirame': 'Flounder Heights', 'kusaya': 'Brinewater Springs',
  'manta': 'Manta Maria', 'nampla': "Um'ami Ruins", 
  'taraport':'Barnacle & Dime', 'kombu': 'Humpback Pump Track',
  'ohyo': 'Shipshape Cargo Co.', 'takaashi': 'Crableg Capital'
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

SPLATSTATS_DTYPES = {
  # Match information -------------------------------------------------------
  'season': 'string',
  #'period': 'datetime64'
  'game-ver': 'string',
  'lobby': 'string',
  'mode': 'string',
  'stage': 'string',
  'time': 'uint16',
  'win': 'bool',
  'knockout': 'Int8',
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


INKSTATS_STYLE = {
    'kill': {
        'color': '#1A1AAEDD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        'range': (0, 15)
    },
    'death': {
        'color': '#801AB3DD', 'range': (0, 15),
        'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .70, 0.95]),
        'range': (0, 15)
    },
    'assist': {
        'color': '#C12D74DD', 'range': (0, 10),
        'scaler': lambda x: np.interp(x, [0, 0.25, 0.65], [0, .70, 0.95]),
        
    },
    'special': {
        'color': '#1FAFE8DD', 'range': (0, 10),
        'scaler': lambda x: np.interp(x, [0, 0.25, 0.65], [0, .70, 0.95]),
    },
    'paint': {
        'color': '#35BA49DD', 'range': (0, 20),
        'scaler': lambda x: np.interp(x, [0, 0.1, 0.2], [0, .70, 0.95]),
    }
}