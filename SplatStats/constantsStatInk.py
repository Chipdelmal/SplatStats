
import json

# with open('./InkStat/stage.json', 'r') as f:
#   WEAPONS = json.load(f)
# wpnKeys = [i['key'] for i in WEAPONS]
# wpnDict = {
#   wpnKeys[ix]: WEAPONS[ix]['name']['en_US'] for ix in range(len(wpnKeys))
# }

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

WPNS_DICT = {
  '52gal': '.52 Gal', '96gal': '.96 Gal', 'bold': 'Sploosh-o-matic',
  'bottlegeyser': 'Squeezer', 'heroshooter_replica': 'Hero Shot Replica',
  'jetsweeper': 'Jet Squelcher', 'momiji': 'Custom Splattershot Jr.',
  'nzap85': "N-ZAP '85", 'prime': 'Splattershot Pro',
  'prime_collabo': 'Forge Splattershot Pro', 'promodeler_mg': 'Aerospray MG',
  'promodeler_rg': 'Aerospray RG', 'sharp': 'Splash-o-matic',
  'spaceshooter': 'Splattershot Nova', 'sshooter': 'Splattershot',
  'sshooter_collabo': 'Tentatek Splattershot', 'wakaba': 'Splattershot Jr.',
  'clashblaster': 'Clash Blaster', 'hotblaster': 'Blaster',
  'longblaster': 'Range Blaster', 'nova': 'Luna Blaster',
  'nova_neo': 'Luna Blaster Neo', 'rapid': 'Rapid Blaster',
  'rapid_elite': 'Rapid Blaster Pro', 'h3reelgun': 'H-3 Nozzlenose',
  'l3reelgun': 'L-3 Nozzlenose', 'dualsweeper': 'Dualie Squelchers',
  'kelvin525': 'Glooga Dualies', 'maneuver': 'Splat Dualies',
  'quadhopper_black': 'Dark Tetra Dualies', 'sputtery': 'Dapple Dualies',
  'sputtery_hue': 'Dapple Dualies Nouveau', 'carbon': 'Carbon Roller',
  'carbon_deco': 'Carbon Roller Deco', 'dynamo': 'Dynamo Roller',
  'splatroller': 'Splat Roller', 'variableroller': 'Flingza Roller',
  'wideroller': 'Big Swig Roller', 'hokusai': 'Octobrush',
  'pablo': 'Inkbrush', 'pablo_hue': 'Inkbrush Nouveau',
  'drivewiper': 'Splatana Wiper', 'jimuwiper': 'Splatana Stamper',
  'bamboo14mk1': 'Bamboozler 14 Mk I', 'liter4k': 'E-liter 4K',
  'liter4k_scope': 'E-liter 4K Scope', 'rpen_5h': 'Snipewriter 5H',
  'soytuber': 'Goo Tuber', 'splatcharger': 'Splat Charger',
  'splatscope': 'Splatterscope', 'squiclean_a': 'Classic Squiffer',
  'bucketslosher': 'Slosher', 'bucketslosher_deco': 'Slosher Deco',
  'explosher': 'Explosher', 'furo': 'Bloblobber',
  'hissen': 'Tri-Slosher', 'screwslosher': 'Sloshing Machine',
  'barrelspinner': 'Heavy Splatling', 'hydra': 'Hydra Splatling',
  'kugelschreiber': 'Ballpoint Splatling', 'nautilus47': 'Nautilus 47',
  'splatspinner': 'Mini Splatling', 'splatspinner_collabo': 'Zink Mini Splatling',
  'campingshelter': 'Tenta Brella', 'parashelter': 'Splat Brella',
  'spygadget': 'Undercover Brella', 'lact450': 'REEF-LUX 450',
  'tristringer': 'Tri-Stringer'
}

STGS_DICT = {
  'yunohana': 'Scorch Gorge', 'gonzui': 'Eeltail Alley',
  'kinmedai': "Museum d'Alfonsino", 'mategai': 'Undertow Spillway',
  'namero': 'Mincemeat Metalworks', 'yagara': 'Hagglefish Market',
  'masaba': 'Hammerhead Bridge', 'mahimahi': 'Mahi-Mahi Resort',
  'zatou': 'MakoMart', 'chozame': 'Sturgeon Shipyard',
  'amabi': 'Inkblot Art Academy', 'sumeshi': 'Wahoo World',
  'hirame': 'Flounder Heights', 'kusaya': 'Brinewater Springs'
}