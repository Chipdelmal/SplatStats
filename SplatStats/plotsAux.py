###############################################################################
# Auxiliary Functions and Constants for Plots
###############################################################################

import SplatStats.colors as clr

# Markers for basic stats
MRKR_STATS = {
    'kill':     'o',
    'death':    'x',
    'assist':   '.',
    'special':  '_'
}

# Markers for match types
MRKR_MT = {
    'Turf War':             '-',
    'Rainmaker':            '1',
    'Splat Zones':          '2',
    'Clam Blitz':           '3',
    'Tower Control':        '4',
    'Tricolor Turf War':    '8'
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