from pygart import make_canvas, solarized_colors, solarized_color, Color_Type
from pygart.util import MGrid
from random import randint, choice, shuffle


# How to plant seeds?
# How to grow seeds?

cells = MGrid(5, 5, lambda: 0)

# plant seeds
# seed number should imply XY which implies the initial seed_populations
SEEDS = 4  # hand picked for (5, 5)
SEED_XY = [(1, 1), (3, 1), (1, 3), (3, 3)]  # hand picked for (5, 5)
SLIME = []
for s, (i, j) in zip(range(SEEDS), SEED_XY):
    cells[i][j] = s + 1
    SLIME.append([[i, j]])


while cells.empty_spaces() > 2 * SEEDS:
# while not cells.full():
    seeds = list(range(SEEDS))
    shuffle(seeds)
    for s in seeds:
        # look for available neighboring cells
        available = []
        for x, y in SLIME[s]:
            for i, j, n in cells.neighbors(x, y):
                if n == 0:
                    available.append((i, j))
        if len(available):
            i, j = choice(available)
            cells[i][j] = s + 1

bgs = solarized_colors(Color_Type.BG_LIGHT)
# How to render image
data = {
        'width': 500,
        'height': 500,
        'w': 500 / 5,
        'weight': 1,
        'bg': bgs[-1],
        'out': bgs[0],
        'fill': None,
        }
image, draw = make_canvas(data)
# Given an ideal grid (5, 5) how to translate to "real" coordinates in (500, 500)
image.save('slime.png')
