
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
# Colors for plots
###############################################################################
# Markers for basic stats
MRKR_STATS = {
    'kill':     'o',
    'death':    'x',
    'assist':   '.',
    'special':  '_'
}
# Markers/Colors for match types
MRKR_MT = {
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
    'Tricolor Turf War':    clr.LPINK_V_BLUE_S2[0]  
}
# Colors for scatter elements
CLR_KILL_DEATH = {
    'kill':  clr.LPINK_V_BLUE_S2[1],
    'death': clr.LPINK_V_BLUE_S2[0]
}
CLR_WIN_LOSE = {
    'W': clr.SKY_V_GOLD_S2[0],
    'L': clr.LBLUE_V_FUCHSIA_S2[1]
}
CLR_PAINT = clr.EATIT_V_SAVEIT_S2[0]

