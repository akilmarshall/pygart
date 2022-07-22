from pygart import info, Canvas, ComplexBox, PaletteRNG, getsu_set
from itertools import product

from random import randint

# scales used: 20, 50, 100, 200
col, row = 6 * 5, 5 * 5

s = 100
r = -s // 2
p = PaletteRNG(list(getsu_set('july'))[0])
canvas = Canvas(*info(), color=p())


def stack(x, y, h, a, b, c, d, e, f):
    '''draw a stack of ComplexBox with h units. '''
    for i in range(h):
        ComplexBox(s, a(), b(), c(), d(), e(), f())(x, y - i * s // 2, canvas)


def fixed():
    c = p
    C = PaletteRNG([p()])
    for x, y in product(range(col), range(row)):
        h, k = r + x * s, r + y * s
        stack(h, k, randint(1, 3), c, c, c, C, C, C)


def rng():
    for x, y in product(range(col), range(row)):
        h, k = r + x * s, r + y * s
        stack(h, k, randint(1, 3), p, p, p, p, p, p)


def none():
    for x, y in product(range(col), range(row)):
        none = PaletteRNG([None])
        h, k = r + x * s, r + y * s
        stack(h, k, randint(1, 3), p, p, p, none, none, none)


fixed()
canvas.save()
