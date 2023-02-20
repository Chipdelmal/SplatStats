###############################################################################
# Chord Analysis
###############################################################################
btlsFiltered = btls[fltrBool]
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
sums = np.sum(matrix, axis=1)

selfProb = np.diag(matrix.copy(), k=0)
norm = colors.LogNorm(vmin=1, vmax=np.max(matrix))
colorPalette = splat.colorPaletteFromHexList(['#bdedf6', '#04067B'])
pColors = [colorPalette(norm(i)) for i in sums]

cMat = matrix.copy()
np.fill_diagonal(cMat, 0)

pad = 1.5
(fig, ax) = plt.subplots(figsize=(10, 10))
ax = chd.chord_modded(
    cMat, names, 
    ax=ax, rotate_names=[True]*len(names),
    fontcolor='k', chordwidth=.7, width=0.1, fontsize=4,
    extent=360, start_at=0,
    colors=pColors, use_gradient=True
)
ax.set_xlim(-pad, pad)
ax.set_ylim(-pad, pad)
ax.axis('off')
fName = 'Chord.png'
plt.savefig(
    path.join('/Users/sanchez.hmsc/Desktop', fName),
    dpi=300, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')

plt.matshow(matrix)


names[0]
sums = np.sum(matrix, axis=1)
(minIx, maxIx) = (
    np.where(sums==sums.min())[0][0],
    np.where(sums==sums.max())[0][0]
)
[names[i] for i in (minIx, maxIx)]

###############################################################################
# Aggregate by date
###############################################################################
df['dummy'] = [1]*df.shape[0]
counts = df.groupby([df['period'].dt.date]).count()['dummy']
(fig, ax) = (plt.figure(), plt.axes())
ax.plot(list(counts))
df['mode'] = [splat.GAME_MODE[lob] for lob in df['mode']]

