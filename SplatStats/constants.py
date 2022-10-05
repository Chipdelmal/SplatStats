
import SplatStats.colors as clr

###############################################################################
# Dataframe-related constants
###############################################################################
BATTLE_DTYPES = {
    'self': bool,       'ko': bool,
    'kill': int,        'death': int,
    'assist': int,      'special': int,
    'splatfest': bool
}
MATCH_TYPES = (
    'Turf War', 'Tower Control', 'Rainmaker', 'Splat Zones', 'Clam Blitz'
)

###############################################################################
# Colors and Markers for plots
###############################################################################
# Markers for basic stats
MKR_STATS = {
    'kill':     'o',
    'death':    'x',
    'assist':   '.',
    'special':  '_'
}
CLR_STATS = {
    'kill':  clr.LPINK_V_BLUE_S2[1],
    'death': clr.LPINK_V_BLUE_S2[0],
    'assist': clr.AUTOBOTS_V_DECEPTICONS[1],
    'special': clr.AUTOBOTS_V_DECEPTICONS[1]
}
# Markers/Colors for match types
MKR_MT = {
    'Turf War':             ',',
    'Rainmaker':            '1',
    'Splat Zones':          '2',
    'Clam Blitz':           '3',
    'Tower Control':        '4',
    'Tricolor Turf War':    '.'
}
CLR_MT = {
    'Turf War':             clr.LMODEL_V_PMODEL_S2[-1],
    'Rainmaker':            clr.WINNERW_V_WOUTERW_S2[2],
    'Splat Zones':          clr.BLUE_V_GREEN_S2[2],
    'Clam Blitz':           clr.RPURPLE_V_GAPPLE_S2[0],
    'Tower Control':        clr.PINK_V_GREEN_S1 [0],
    'Tricolor Turf War':    clr.PINK_V_GREEN_S1 [0]  
}
CLR_PAINT = clr.TURQUOISE_V_PUMPKIN_S2[-1]
# Colors for scatter elements
CLR_WL = {
    'W': clr.SKY_V_GOLD_S2[0],
    'L': clr.LBLUE_V_FUCHSIA_S2[1]
}
MKR_WL = {
    'W': '^',
    'L': 'v'
}
MKR_KO = {
    True: '.',
    False: ','    
}
CLR_KO = {
    True: clr.SKY_V_GOLD_S2[0],
    False: clr.LMODEL_V_PMODEL_S2[-1]
}
MKR_FEST = {
    True: '.',
    False: ','
}
CLR_FEST = {
    True: clr.PINK_V_GREEN_S1 [0],
    False: clr.LMODEL_V_PMODEL_S2[-1]
}
CLR_STAGE = {
    'Inkblot Art Academy': clr.LPINK_V_BLUE_S2[0],
    'Hagglefish Market': clr.LPINK_V_BLUE_S2[1],
    'MakoMart': clr.PINK_V_GREEN_S1[2],
    'Eeltail Alley': clr.PINK_V_ORANGE_S1[1],
    'Wahoo World': clr.PINK_V_ORANGE_S1[2],
    'Undertow Spillway': clr.RASPBERRY_V_NYELLOW_S2[1],
    'Mahi-Mahi Resort': clr.CHAOS_V_ORDER_S2[1],
    'Hammerhead Bridge': clr.MAYO_V_KETCHUP_S2[1],
    'Sturgeon Shipyard': clr.VAMPIRE_V_WEREWOLF_S2[2],
    'Mincemeat Metalworks': clr.TSUBUAN_V_KOSHIAN_S2[1],
    "Museum d'Alfonsino": clr.SALTY_V_SWEET_S2[0],
    'Scorch Gorge': clr.UNICORN_V_NARWHAL_S2[0]
}
CLR_CLS_LONG = [
    clr.LPINK_V_BLUE_S2[0], clr.LPINK_V_BLUE_S2[1],
    clr.NPINK_V_NGREEN_S2[1], 
    clr.RASPBERRY_V_NYELLOW_S2[1],
    clr.WINNERW_V_WOUTERW_S2[0], clr.WINNERW_V_WOUTERW_S2[1], clr.WINNERW_V_WOUTERW_S2[2],
    clr.TSUBUAN_V_KOSHIAN_S2[1],
    clr.FAM_V_FRIEND_S2[1],
    clr.GRAPE_V_TURQUOISE_S2[0], clr.GRAPE_V_TURQUOISE_S2[1]
]