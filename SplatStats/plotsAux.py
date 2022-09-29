###############################################################################
# Auxiliary Functions and Constants for Plots
###############################################################################

import numpy as np
from colorutils import Color


def mapNumberToSaturation(
        num, colorHex, 
        numLims=(0, 15, 50), satLims=(0, .1, 1)
    ):
    """Linearly maps a variable within a range (numLim) to the saturation value of a color.

    Args:
        num (float): Number in the (numLim) range.
        colorHex (str): Color of which the saturation will be changed.
        numLims (tuple, optional): Range of values the number can take. Defaults to (0, 15, 50).
        satLims (tuple, optional): Range of saturations the values will be linearly mapped to. Defaults to (0, 1, 1).

    Returns:
        str: Hex of the new color with saturation changed dependent on the number value.
    """    
    iPol = np.interp(num, numLims, satLims)
    kCol = Color(hex=colorHex)
    kOut = Color(hsv=(kCol.hsv[0], iPol, kCol.hsv[1]))
    return kOut.hex


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)