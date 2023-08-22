"""
NOT MY CODE!!!!!!!!!

Extended from: https://github.com/tfardet/mpl_chord_diagram/blob/main/chord_diagram.py
Tools to draw a chord diagram in python
"""

from collections.abc import Sequence
import matplotlib.patches as patches
from matplotlib.colors import ColorConverter
from matplotlib.path import Path
import numpy as np
import scipy.sparse as ssp
from collections import defaultdict
import numpy as np



def chord_modded(mat, names=None, order=None, width=0.1, pad=2., gap=0.03,
                  chordwidth=0.7, ax=None, colors=None, cmap=None, alpha=0.7,
                  use_gradient=False, chord_colors=None, start_at=0, extent=360,
                  directed=False, show=False, **kwargs):
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots()

    # copy matrix
    is_sparse = ssp.issparse(mat)

    if is_sparse:
        mat = mat.tocsr(copy=True)
    else:
        mat = np.array(mat, copy=True)

    num_nodes = mat.shape[0]

    # don't use gradient with directed chords
    use_gradient *= not directed

    # set min entry size for small entries and zero reciprocals
    # mat[i, j]:  i -> j
    min_deg = kwargs.get("min_chord_width", 0)

    if is_sparse and min_deg:
        nnz = mat.nonzero()

        mat.data[mat.data < min_deg] = min_deg

        # check zero reciprocals
        for i, j in zip(*nnz):
            if mat[j, i] < min_deg:
                mat[j, i] = min_deg
    else:
        nnz = mat > 0

        mat[nnz] = np.maximum(mat[nnz], min_deg)

        # check zero reciprocals
        for i, j in zip(*np.where(~nnz)):
            if mat[j, i]:
                mat[i, j] = min_deg

    # check name rotations
    rotate_names = kwargs.get("rotate_names", False)

    if isinstance(rotate_names, Sequence):
        assert len(rotate_names) == num_nodes, \
            "Wrong number of entries in 'rotate_names'."
    else:
        rotate_names = [rotate_names]*num_nodes

    # check order
    if order is not None:
        mat = mat[order][:, order]

        rotate_names = [rotate_names[i] for i in order]

        if names is not None:
            names = [names[i] for i in order]

        if colors is not None:
            colors = [colors[i] for i in order]

    # configure colors
    if colors is None:
        colors = np.linspace(0, 1, num_nodes)

    fontcolor = kwargs.get("fontcolor", "k")

    if isinstance(fontcolor, str):
        fontcolor = [fontcolor]*num_nodes
    else:
        assert len(fontcolor) == num_nodes, \
            "One fontcolor per node is required."

    if cmap is None:
        cmap = "viridis"

    if isinstance(colors, (list, tuple, np.ndarray)):
        assert len(colors) == num_nodes, "One color per node is required."

        # check color type
        first_color = colors[0]

        if isinstance(first_color, (int, float, np.integer)):
            cm = plt.get_cmap(cmap)
            colors = cm(colors)[:, :3]
        else:
            colors = [ColorConverter.to_rgb(c) for c in colors]
    else:
        raise ValueError("`colors` should be a list.")

    if chord_colors is None:
       chord_colors = colors
    else:
        try:
            chord_colors = [ColorConverter.to_rgb(chord_colors)] * num_nodes
        except ValueError:
            assert len(chord_colors) == num_nodes, \
                "If `chord_colors` is a list of colors, it should include " \
                "one color per node (here {} colors).".format(num_nodes)

    # sum over rows
    out_deg = mat.sum(axis=1).A1 if is_sparse else mat.sum(axis=1)
    in_deg = None
    degree = out_deg.copy()

    if directed:
        # also sum over columns
        in_deg = mat.sum(axis=0).A1 if is_sparse else mat.sum(axis=0)
        degree += in_deg

    pos = {}
    pos_dir = {}
    arc = []
    nodePos = []
    rotation = []

    # compute all values and optionally apply sort
    compute_positions(mat, degree, in_deg, out_deg, start_at, is_sparse, kwargs,
                      directed, extent, pad, arc, rotation, nodePos, pos)

    # plot
    for i in range(num_nodes):
        color = colors[i]

        # plot the arcs
        start_at, end = arc[i]

        ideogram_arc(start=start_at, end=end, radius=1.0, color=color,
                     width=width, alpha=alpha, ax=ax)

        chord_color = chord_colors[i]

        # plot self-chords if directed is False
        if not directed and mat[i, i]:
            start1, end1, _, _ = pos[(i, i)]
            self_chord_arc(start1, end1, radius=1 - width - gap,
                           chordwidth=0.7*chordwidth, color=chord_color,
                           alpha=alpha, ax=ax)

        # plot all other chords
        targets = range(num_nodes) if directed else range(i)

        for j in targets:
            cend = chord_colors[j]

            start1, end1, start2, end2 = pos[(i, j)]

            if mat[i, j] > 0 or (not directed and mat[j, i] > 0):
                chord_arc(
                    start1, end1, start2, end2, radius=1 - width - gap, gap=gap,
                    chordwidth=chordwidth, color=chord_color, cend=cend,
                    alpha=alpha, ax=ax, use_gradient=use_gradient,
                    extent=extent, directed=directed)

    # add names if necessary
    if names is not None:
        assert len(names) == num_nodes, "One name per node is required."

        prop = {
            "fontsize": kwargs.get("fontsize", 16*0.8),
            "ha": "center",
            "va": "center",
            "rotation_mode": "anchor"
        }

        for i, (pos, name, r) in enumerate(zip(nodePos, names, rotation)):
            rotate = rotate_names[i]
            pp = prop.copy()
            pp["color"] = fontcolor[i]

            if rotate:
                angle  = np.average(arc[i])
                rotate = 90

                if 90 < angle < 180 or 270 < angle:
                    rotate = -90

                if 90 < angle < 270:
                    pp["ha"] = "right"
                else:
                    pp["ha"] = "left"
            elif r:
                pp["va"] = "top"
            else:
                pp["va"] = "bottom"

            ax.text(pos[0], pos[1], name, rotation=pos[2] + rotate, **pp)

    # configure axis
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

    ax.set_aspect(1)
    # ax.axis('off')

    # plt.tight_layout()

    if show:
        plt.show()

    return ax


# ------------ #
# Subfunctions #
# ------------ #

def initial_path(start, end, radius, width, factor=4/3):
    ''' First 16 vertices and 15 instructions are the same for everyone '''
    if start > end:
        start, end = end, start

    start *= np.pi/180.
    end   *= np.pi/180.

    # optimal distance to the control points
    # https://stackoverflow.com/questions/1734745/
    # how-to-create-circle-with-b%C3%A9zier-curves
    # use 16-vertex curves (4 quadratic Beziers which accounts for worst case
    # scenario of 360 degrees)
    inner = radius*(1-width)
    opt   = factor * np.tan((end-start)/ 16.) * radius
    inter1 = start*(3./4.)+end*(1./4.)
    inter2 = start*(2./4.)+end*(2./4.)
    inter3 = start*(1./4.)+end*(3./4.)

    verts = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start+0.5*np.pi),
        polar2xy(radius, inter1) + polar2xy(opt, inter1-0.5*np.pi),
        polar2xy(radius, inter1),
        polar2xy(radius, inter1),
        polar2xy(radius, inter1) + polar2xy(opt, inter1+0.5*np.pi),
        polar2xy(radius, inter2) + polar2xy(opt, inter2-0.5*np.pi),
        polar2xy(radius, inter2),
        polar2xy(radius, inter2),
        polar2xy(radius, inter2) + polar2xy(opt, inter2+0.5*np.pi),
        polar2xy(radius, inter3) + polar2xy(opt, inter3-0.5*np.pi),
        polar2xy(radius, inter3),
        polar2xy(radius, inter3),
        polar2xy(radius, inter3) + polar2xy(opt, inter3+0.5*np.pi),
        polar2xy(radius, end) + polar2xy(opt, end-0.5*np.pi),
        polar2xy(radius, end)
    ]

    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    return start, end, verts, codes


def ideogram_arc(start, end, radius=1., width=0.2, color="r", alpha=0.7,
                 ax=None):
    '''
    Draw an arc symbolizing a region of the chord diagram.

    Parameters
    ----------
    start : float (degree in 0, 360)
        Starting degree.
    end : float (degree in 0, 360)
        Final degree.
    radius : float, optional (default: 1)
        External radius of the arc.
    width : float, optional (default: 0.2)
        Width of the arc.
    ax : matplotlib axis, optional (default: not plotted)
        Axis on which the arc should be plotted.
    color : valid matplotlib color, optional (default: "r")
        Color of the arc.

    Returns
    -------
    verts, codes : lists
        Vertices and path instructions to draw the shape.
    '''
    start, end, verts, codes = initial_path(start, end, radius, width)

    opt    = 4./3. * np.tan((end-start)/ 16.) * radius
    inner  = radius*(1-width)
    inter1 = start*(3./4.) + end*(1./4.)
    inter2 = start*(2./4.) + end*(2./4.)
    inter3 = start*(1./4.) + end*(3./4.)

    verts += [
        polar2xy(inner, end),
        polar2xy(inner, end) + polar2xy(opt*(1-width), end-0.5*np.pi),
        polar2xy(inner, inter3) + polar2xy(opt*(1-width), inter3+0.5*np.pi),
        polar2xy(inner, inter3),
        polar2xy(inner, inter3),
        polar2xy(inner, inter3) + polar2xy(opt*(1-width), inter3-0.5*np.pi),
        polar2xy(inner, inter2) + polar2xy(opt*(1-width), inter2+0.5*np.pi),
        polar2xy(inner, inter2),
        polar2xy(inner, inter2),
        polar2xy(inner, inter2) + polar2xy(opt*(1-width), inter2-0.5*np.pi),
        polar2xy(inner, inter1) + polar2xy(opt*(1-width), inter1+0.5*np.pi),
        polar2xy(inner, inter1),
        polar2xy(inner, inter1),
        polar2xy(inner, inter1) + polar2xy(opt*(1-width), inter1-0.5*np.pi),
        polar2xy(inner, start) + polar2xy(opt*(1-width), start+0.5*np.pi),
        polar2xy(inner, start),
        polar2xy(radius, start),
    ]

    codes += [
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]

    if ax is not None:
        path  = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color, alpha=alpha,
                                  edgecolor=color, lw=LW)
        ax.add_patch(patch)

    return verts, codes


def chord_arc(start1, end1, start2, end2, radius=1.0, gap=0.03, pad=2,
              chordwidth=0.7, ax=None, color="r", cend="r", alpha=0.7,
              use_gradient=False, extent=360, directed=False):
    '''
    Draw a chord between two regions (arcs) of the chord diagram.

    Parameters
    ----------
    start1 : float (degree in 0, 360)
        Starting degree.
    end1 : float (degree in 0, 360)
        Final degree.
    start2 : float (degree in 0, 360)
        Starting degree.
    end2 : float (degree in 0, 360)
        Final degree.
    radius : float, optional (default: 1)
        External radius of the arc.
    gap : float, optional (default: 0)
        Distance between the arc and the beginning of the cord.
    chordwidth : float, optional (default: 0.2)
        Width of the chord.
    ax : matplotlib axis, optional (default: not plotted)
        Axis on which the chord should be plotted.
    color : valid matplotlib color, optional (default: "r")
        Color of the chord or of its beginning if `use_gradient` is True.
    cend : valid matplotlib color, optional (default: "r")
        Color of the end of the chord if `use_gradient` is True.
    alpha : float, optional (default: 0.7)
        Opacity of the chord.
    use_gradient : bool, optional (default: False)
        Whether a gradient should be use so that chord extremities have the
        same color as the arc they belong to.
    extent : float, optional (default : 360)
        The angular aperture, in degrees, of the diagram.
        Default is to use the whole circle, i.e. 360 degrees, but in some cases
        it can be useful to use only a part of it.
    directed : bool, optional (default: False)
        Whether the chords should be directed, ending in an arrow.

    Returns
    -------
    verts, codes : lists
        Vertices and path instructions to draw the shape.
    '''
    chordwidth2 = chordwidth

    dtheta1 = min((start1 - end2) % extent, (end2 - start1) % extent)
    dtheta2 = min((end1 - start2) % extent, (start2 - end1) % extent)

    start1, end1, verts, codes = initial_path(start1, end1, radius, chordwidth)

    if directed:
        if start2 > end2:
            start2, end2 = end2, start2

        start2 *= np.pi/180.
        end2   *= np.pi/180.

        tip = 0.5*(start2 + end2)
        asize = max(gap, 0.02)

        verts2 = [
            polar2xy(radius - asize, start2),
            polar2xy(radius, tip),
            polar2xy(radius - asize, end2)
        ]
    else:
        start2, end2, verts2, _ = initial_path(start2, end2, radius, chordwidth)

    chordwidth2 *= np.clip(0.4 + (dtheta1 - 2*pad) / (15*pad), 0.2, 1)

    chordwidth *= np.clip(0.4 + (dtheta2 - 2*pad) / (15*pad), 0.2, 1)

    rchord  = radius * (1-chordwidth)
    rchord2 = radius * (1-chordwidth2)

    verts += [polar2xy(rchord, end1), polar2xy(rchord, start2)] + verts2

    verts += [
        polar2xy(rchord2, end2),
        polar2xy(rchord2, start1),
        polar2xy(radius, start1),
    ]

    # update codes

    codes += [
        Path.CURVE4,
        Path.CURVE4,
    ]

    if directed:
        codes += [
            Path.CURVE4,
            Path.LINETO,
            Path.LINETO,
        ]
    else:
        codes += [
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
        ]

    codes += [
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    if ax is not None:
        path = Path(verts, codes)

        if use_gradient:
            # find the start and end points of the gradient
            points, min_angle = None, None

            if dtheta1 < dtheta2:
                points = [
                    polar2xy(radius, start1),
                    polar2xy(radius, end2),
                ]

                min_angle = dtheta1
            else:
                points = [
                    polar2xy(radius, end1),
                    polar2xy(radius, start2),
                ]

                min_angle = dtheta1

            # make the patch
            patch = patches.PathPatch(path, facecolor="none",
                                      edgecolor="none", lw=LW)
            ax.add_patch(patch)  # this is required to clip the gradient

            # make the grid
            x = y = np.linspace(-1, 1, 100)
            meshgrid = np.meshgrid(x, y)

            gradient(points[0], points[1], min_angle, color, cend, meshgrid,
                     patch, ax, alpha)
        else:
            patch = patches.PathPatch(path, facecolor=color, alpha=alpha,
                                      edgecolor=color, lw=LW)

            idx = 16

            ax.add_patch(patch)

    return verts, codes


def self_chord_arc(start, end, radius=1.0, chordwidth=0.7, ax=None,
                   color=(1,0,0), alpha=0.7):
    start, end, verts, codes = initial_path(start, end, radius, chordwidth)

    rchord = radius * (1 - chordwidth)

    verts += [
        polar2xy(rchord, end),
        polar2xy(rchord, start),
        polar2xy(radius, start),
    ]

    codes += [
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    if ax is not None:
        path  = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color, alpha=alpha,
                                  edgecolor=color, lw=LW)
        ax.add_patch(patch)

    return verts, codes


"""
Create linear color gradients
"""

from matplotlib.colors import ColorConverter, LinearSegmentedColormap
from scipy.ndimage import gaussian_filter

import numpy as np




def dist(points):
    '''
    Compute the distance between two points.

    Parameters
    ----------
    points : array of length 4
        The coordinates of the two points, P1 = (x1, y1) and P2 = (x2, y2)
        in the order [x1, y1, x2, y2].
    '''
    x1, y1 = points[0]
    x2, y2 = points[1]

    return np.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))


def polar2xy(r, theta):
    '''
    Convert the coordinates of a point P from polar (r, theta) to cartesian
    (x, y).
    '''
    return np.array([r*np.cos(theta), r*np.sin(theta)])


def compute_positions(mat, deg, in_deg, out_deg, start_at, is_sparse, kwargs,
                      directed, extent, pad, arc, rotation, nodePos, pos):
    '''
    Compute all arcs and chords start/end positions.

    Parameters
    ----------
    mat : matrix
        Original matrix.
    deg : array
        Out (if undirected) or total (if directed) degree to compute the
        starting positions.
    in_deg : array
        In-degree to compute the end positions (if directed).
    out_deg : array
        Out-degree to compute the end positions (if directed).
    y : array
        Used to compute the arcs' ends.
    start_at : float
        Start of the first arc.
    is_sparse : bool
        Whether the matrix is sparse.
    kwargs : dict
        Keyword arguments.
    directed : bool
        Whether the chords are directed.
    extent : float in ]0, 360]
        Angular aperture of the diagram.
    pad : float
        Gap between entries.
    arc : list
        Used to store the arcs start and endpoints.
    rotation : list
        Store the rotation booleans for the names.
    nodePos : list
        Store the name positions.
    pos : dict
        Store the start and end positions for each arc under the form:
        (start1, end1, start2, end2), where (start1, end1) are the limits of the
        chords starting point, and (start2, end2) are the limits of the chord's
        end point.
    '''
    num_nodes = len(deg)

    # find position for each start and end
    y = deg / np.sum(deg).astype(float) * (extent - pad * num_nodes)

    if directed:
        y_out = out_deg / np.sum(deg).astype(float) * (extent - pad * num_nodes)

    starts = [start_at] + (
        start_at + np.cumsum(y + pad*np.ones(num_nodes))).tolist()

    out_ends = [s + d for s, d in zip(starts, (y_out if directed else y))]


    # relative positions within an arc
    zmat = [
        _get_normed_line(mat, i, out_deg if directed else deg, starts[i],
                         out_ends[i], is_sparse)
        for i in range(num_nodes)
    ]

    zin_mat = zmat

    if directed:
        zin_mat = [
            _get_normed_line(mat.T, i, in_deg, out_ends[i], starts[i + 1] - pad,
                             is_sparse)
            for i in range(num_nodes)
        ]

    # sort
    sort = kwargs.get("sort", "size")

    mat_ids = _get_sorted_ids(sort, zmat, num_nodes, directed)

    # compute positions
    for i in range(num_nodes):
        # arcs
        start = starts[i]
        end = start + y[i]
        arc.append((start, end))
        angle = 0.5*(start + end)

        if -30 <= (angle % 360) <= 180:
            angle -= 90
            rotation.append(False)
        else:
            angle -= 270
            rotation.append(True)

        nodePos.append(
            tuple(polar2xy(1.05, 0.5*(start + end)*np.pi/180.)) + (angle,))

        # sort chords
        z = zmat[i]
        z0 = start

        for j in mat_ids[i]:
            # compute the arrival points
            zj = zin_mat[j]
            startj = out_ends[j] if directed else starts[j]

            jids = mat_ids[j]

            distsort = (sort == "distance")

            if directed and not distsort:
                jids = jids[::-1]

            stop = np.where(np.equal(jids, i))[0][0]

            startji = startj + zj[jids[:stop]].sum()

            if distsort and directed:
                # we want j first for target positions
                startji += zj[j]

            if distsort and directed and i == j:
                pos[(i, j)] = (z0, z0 + z[j], startj, startj + zj[j])
            else:
                pos[(i, j)] = (z0, z0 + z[j], startji, startji + zj[jids[stop]])

            z0 += z[j]


# In-file functions

def _get_normed_line(mat, i, x, start, end, is_sparse):
    if is_sparse:
        row = mat.getrow(i).todense().A1
        return (row / x[i]) * (end - start)

    return (mat[i, :] / x[i]) * (end - start)


def _get_sorted_ids(sort, zmat, num_nodes, directed):
    mat_ids = defaultdict(lambda: list(range(num_nodes)))

    if sort == "size":
        mat_ids = [np.argsort(z) for z in zmat]
    elif sort == "distance":
        mat_ids = []
        for i in range(num_nodes):
            remainder = 0 if num_nodes % 2 else -1

            ids  = list(range(i - int(0.5*num_nodes), i))[::-1]

            if not directed:
                ids += [i]

            ids += list(range(i + int(0.5*num_nodes) + remainder, i, -1))

            if directed:
                ids += [i]

            # put them back into [0, num_nodes[
            ids = np.array(ids)
            ids[ids < 0] += num_nodes
            ids[ids >= num_nodes] -= num_nodes

            mat_ids.append(ids)
    elif sort is not None:
        raise ValueError("Invalid `sort`: '{}'".format(sort))

    return mat_ids


LW = 0.3


def linear_gradient(cstart, cend, n=10):
    '''
    Return a gradient list of `n` colors going from `cstart` to `cend`.
    '''
    s = np.array(ColorConverter.to_rgb(cstart))
    f = np.array(ColorConverter.to_rgb(cend))

    rgb_list = [s + (t / (n - 1))*(f - s) for t in range(n)]

    return rgb_list


def gradient(start, end, min_angle, color1, color2, meshgrid, mask, ax,
             alpha):
    '''
    Create a linear gradient from `start` to `end`, which is translationally
    invarient in the orthogonal direction.
    The gradient is then cliped by the mask.
    '''
    xs, ys = start
    xe, ye = end

    X, Y = meshgrid

    # get the distance to each point
    d2start = (X - xs)*(X - xs) + (Y - ys)*(Y - ys)
    d2end   = (X - xe)*(X - xe) + (Y - ye)*(Y - ye)

    dmax = (xs - xe)*(xs - xe) + (ys - ye)*(ys - ye)

    # blur
    smin = 0.015*len(X)
    smax = max(smin, 0.1*len(X)*min(min_angle/120, 1))

    sigma = np.clip(dmax*len(X), smin, smax)

    Z = gaussian_filter((d2end < d2start).astype(float), sigma=sigma)

    # generate the colormap
    n_bin = 100

    color_list = linear_gradient(color1, color2, n_bin)

    cmap = LinearSegmentedColormap.from_list("gradient", color_list, N=n_bin)

    im = ax.imshow(Z, interpolation='bilinear', cmap=cmap,
                   origin='lower', extent=[-1, 1, -1, 1], alpha=alpha)

    im.set_clip_path(mask)