from itertools import cycle, product
from random import random, shuffle

from aggdraw import Brush, Draw, Pen

from pygart import Canvas, PaletteRNG, V, getsu_set, info
from perlin_noise import PerlinNoise
from math import sin, pi


class Figure:
    def __init__(self, pallete: PaletteRNG): 
        '''
        :u:         unit length
        '''
        self.p = pallete

    def config(self, u):
        self.u = u

    def setup(self, x: int, y: int): 
        u = self.u
        i = V(u, 0)
        j = V(0, u)
        self.root = root = V(x, y)
        self.A = root + i
        self.B = root + (i + j) / 5
        self.C = self.B + 3 * i / 5
        self.D = self.B + (i + j) / 10
        self.E = self.D + 2 * i / 5
        self.F = self.D + 2 * j / 5
        self.G = self.F + 2 * i / 5
        self.H = self.B + 3 * j / 5
        self.I = self.H + 3 * i / 5
        self.J = root + j
        self.K = self.J + i
        self.L = self.root + 5 * (i + j) / 100
        self.M = self.L + 9 * i / 10
        self.N = self.M + 9 * j / 10
        self.O = self.L + 9 * j / 10

    def colors(self, N=5):
        shuffle(self.p.colors)
        for _, c in zip(range(N), cycle(self.p.colors)):
            yield c

    def pen(self, c, w=1):
        return Pen(c, w)

    def brush(self, c):
        return Brush(c)

    def draw(self, img):
        draw = Draw(img)
        a, b, c, d, e, *_  = self.colors()
        draw.polygon((*self.root(), *self.A(), *self.M(), *self.L(), *self.O(), *self.J()), self.brush(b))
        draw.polygon((*self.O(), *self.N(), *self.K(), *self.J()), self.brush(d))
        draw.polygon((*self.A(), *self.K(), *self.N(), *self.M()), self.brush(c))
        draw.polygon((*self.L(), *self.M(), *self.N(), *self.O()), self.brush(a))
        draw.polygon((*self.B(), *self.C(), *self.E(), *self.D()), self.brush(c))
        draw.polygon((*self.E(), *self.C(), *self.I(), *self.H(), *self.F(), *self.G()), self.brush(b))
        draw.polygon((*self.B(), *self.D(), *self.F(), *self.H()), self.brush(d))
        draw.polygon((*self.D(), *self.E(), *self.G(), *self.F()), self.brush(a))
        draw.line((*self.root(), *self.L()), self.pen(e))
        draw.line((*self.B(), *self.D()), self.pen(e))
        draw.line((*self.G(), *self.I()), self.pen(e))
        draw.line((*self.G(), *self.I()), self.pen(e))
        draw.line((*self.N(), *self.K()), self.pen(e))

        draw.line((*self.A(), *self.M()), self.pen(e))
        draw.line((*self.C(), *self.E()), self.pen(e))
        draw.line((*self.F(), *self.H()), self.pen(e))
        draw.line((*self.O(), *self.J()), self.pen(e))
        draw.flush()


class Tiling:
    def __init__(self, fig: Figure, u, cols, rows):
        self.fig = fig
        self.u = u
        self.cols = cols
        self.rows = rows

    def ordered_points(self):
        """Traverse the tiling left to right, top to bottom. """
        for i, j in product(range(self.cols + 1), range(self.rows + 1)):
            yield (V(i, j) * self.u)()

    def perlin_ordered(self):
        """
        Associate a perlin noise field onto a tiling,
        return the list ordered by noise value.
        """
        field = PerlinNoise(octaves=0.25)
        points = []
        for x, y in self.ordered_points():
            amplitude = field([x / self.cols, y / self.rows])
            points += [(amplitude, x, y)]
        points.sort()
        for _, x, y in points:
            yield (x, y)

    def wave_ordered(self, speed: float = 0.07, shift: float = 200):
        points = []
        wave = lambda x: sin(shift + speed * x) 
        for x, y in self.ordered_points():
            i = x / self.cols
            points += [(wave(2 * pi * i), x, y)]
        points.sort()
        for a, x, y in points:
            yield (a, x, y)

    def tile(self, img, fname='out.png'):
        for a, i, j in self.wave_ordered():
            # delta = a * self.u  # random unit size
            self.fig.config(1.25 * self.u - (self.u / 3) * a)
            self.fig.setup(i, j)
            self.fig.draw(img)
        canvas.save(fname)

width, height, i = info()

i = int(i)  # pallette index
colors = list(getsu_set('september'))[i]
p = PaletteRNG(colors)
canvas = Canvas(width, height, color=p())
usize = 10  # for unit size
cols = width // usize
rows = height // usize
Tiling(Figure(p), usize, cols, rows).tile(canvas.img) 
# what if the tiling took place in a random order and each unit form was a slightly different size
