
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
    'Turf War':             '-',
    'Rainmaker':            '1',
    'Splat Zones':          '2',
    'Clam Blitz':           '3',
    'Tower Control':        '4',
    'Tricolor Turf War':    '.'
}
CLR_MT = {
    'Turf War':             clr.BLUE_V_GREEN_S2[0],
    'Rainmaker':            clr.WINNERW_V_WOUTERW_S2[2],
    'Splat Zones':          clr.BLUE_V_GREEN_S2[2],
    'Clam Blitz':           clr.RPURPLE_V_GAPPLE_S2[0],
    'Tower Control':        clr.CHAOS_V_ORDER_S2[2],
    'Tricolor Turf War':    clr.KID_V_GROWUP_S2[0]  
}
CLR_PAINT = clr.EATIT_V_SAVEIT_S2[0]
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
    False: '-'    
}
CLR_KO = {
    True: clr.SKY_V_GOLD_S2[0],
    False: clr.LBLUE_V_FUCHSIA_S2[1]
}
MKR_FEST = {
    True: '.',
    False: '-'
}
CLR_FEST = {
    True: clr.KID_V_GROWUP_S2[0],
    False: clr.CHICKEN_V_EGG_S2[0]
}