from itertools import product
from math import cos, pi, sin

from aggdraw import Draw, Pen, Brush

from pygart import Canvas, PaletteRNG, V, parameters, month_palette, line, PaletteOrdered, ground_colors
from random import shuffle, choice, random

def shuffle_cycle(lst):
    while True:
        for l in lst:
            yield l
        shuffle(lst)

def S(magnitude, theta):
    """Action. """
    return V(magnitude * cos(theta), magnitude * sin(theta))

class Figure:
    def __init__(self, bg, colors:list): 
        '''
        :u:         unit length
        '''
        self.bg = bg
        self.c = colors
        self.p = PaletteRNG(colors)
        self.o = PaletteOrdered(colors)

    def config(self, r, w):
        self.r = r
        self.w = w

    def setup(self, x, y, theta:float): 
        r = self.r
        root = self.root = V(x, y)
        self.A = root + S(r, (pi / 6) + theta) 
        self.B = root + S(r, (5 * pi / 6) + theta)
        self.C = root + S(r, (7 * pi / 6) + theta)
        self.D = root + S(r, (11 * pi / 6) + theta)

        # self.Ai = root + S(0.8 * r, (pi / 6) + theta) 
        # self.Bi = root + S(0.8 * r, (5 * pi / 6) + theta)
        # self.Ci = root + S(0.8 * r, (7 * pi / 6) + theta)
        # self.Di = root + S(0.8 * r, (11 * pi / 6) + theta)

    def pen(self, c):
        return Pen(c, self.w)

    def brush(self):
        return Brush(self.bg)

    def colors(self):
        # c1, c2, c3, = (self.p_ordered(), self.p_ordered(), self.p_ordered())
        c1, c2, c3, = (self.p(), self.p(), self.p())
        # c1 = c2 = c3 = self.p()
        return c1, c2, c3

    def draw(self, draw):
        c1, c2, c3, = self.colors()
        # outline
        draw.polygon((*self.A(), *self.B(), *self.C(), *self.D()), self.pen(c1), self.brush())

    def __call__(self, draw):
        self.draw(draw)


def grid_points(cols, rows, u):
    dx = u * 2 * cos(pi / 6)
    dy = 3 * u / 2
    for i, j in product(range(cols), range(rows)):
        off = 0
        if j % 2 == 1:
            off = dx / 2
        yield dx * i + off, dy * j

def points(width, height, n):
    for _ in range(n):
        x = width * random()
        y = height * random()
        yield x, y

args = parameters(WIDTH=600, HEIGHT=600)
bg, colors = ground_colors(list(month_palette(args.month, args.p)))
shuffle(colors)
# bg, *colors = all_colors
p = PaletteRNG(colors)
canvas = Canvas(args.width, args.height, color=bg)
draw = Draw(canvas.img)

u = 30 
rows = 1 + (args.width // u)
cols = 1 + (args.height // u)

w = 2
fig = Figure(bg, colors)
fig.config(u, w)
# fig.setup(args.width / 2, args.height / 2, 0 * pi / 3)
# fig(draw)
layers = 5
for l in range(layers):
    for x, y in points(args.width, args.height, 500):
        fig.setup(x, y, choice([0, pi/6, 5*pi/6, pi/3, 2*pi/3])) 
        fig(draw)
draw.flush()
canvas.save(args.out)
