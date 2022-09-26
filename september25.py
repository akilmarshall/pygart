from itertools import product, cycle
from math import cos, pi, sin

from aggdraw import Draw, Pen

from pygart import Canvas, PaletteRNG, V, parameters, month_palette, line, PaletteOrdered
from random import shuffle

def shuffle_cycle(lst):
    while True:
        for l in lst:
            yield l
        shuffle(lst)

def S(magnitude, theta):
    """Action. """
    return V(magnitude * cos(theta), magnitude * sin(theta))

class FigureA:
    def __init__(self, palette: PaletteRNG, w=2): 
        '''
        :u:         unit length
        '''
        self.p = palette
        self.p_ordered = PaletteOrdered(palette.colors)
        self.w = w

    def config(self, u, outline=True):
        self.u = u
        self.outline = outline

    def setup(self, x: int, y: int, n=7): 
        """
        n points on the line segments, cross and inner
        """
        u = self.u
        root = self.root = V(x, y)
        self.A = root + S(u, pi / 6) 
        self.B = root + S(u, pi / 2)
        self.C = root + S(u, 5 * pi / 6)
        self.D = root + S(u, 7 * pi / 6)
        self.E = root + S(u, 3 * pi / 2)
        self.F = root + S(u, 11 * pi / 6) 

        self.EF = line(self.E(), self.F(), n + 2)[1:-1]
        self.FE = line(self.F(), self.E(), n + 2)[1:-1]
        self.DC = line(self.D(), self.C(), n + 2)[1:-1]
        self.AB = line(self.A(), self.B(), n + 2)[1:-1]
        self.BA = line(self.B(), self.A(), n + 2)[1:-1]
        self.ED = line(self.E(), self.D(), n + 2)[1:-1]
        self.DE = line(self.D(), self.E(), n + 2)[1:-1]
        self.FA = line(self.F(), self.A(), n + 2)[1:-1]
        self.BC = line(self.B(), self.C(), n + 2)[1:-1]
        self.CB = line(self.C(), self.B(), n + 2)[1:-1]

        self.rootE = line(self.root(), self.E(), n + 2)[1:-1]
        self.rootC = line(self.root(), self.C(), n + 2)[1:-1]
        self.rootA = line(self.root(), self.A(), n + 2)[1:-1]

    def pen(self, c, s=1):
        return Pen(c, s * self.w)

    def colors(self):
        # c1, c2, c3, = (self.p_ordered(), self.p_ordered(), self.p_ordered())
        c1 = c2 = c3 = self.p()
        return c1, c2, c3

    def draw(self, img):
        draw = Draw(img)
        c1, c2, c3, = self.colors()
        # outline
        if self.outline:
            draw.polygon((*self.A(), *self.B(), *self.C(), *self.D(), *self.E(), *self.F()), self.pen(c))

        # cross lines
        for a, b in zip(self.EF, self.DC):
            draw.line((*a(), *b()), self.pen(c1))

        for a, b in zip(self.EF, self.BA):
            draw.line((*a(), *b()), self.pen(c2))

        for a, b in zip(self.DC, self.AB):
            draw.line((*a(), *b()), self.pen(c3))

        draw.flush()

class FigureB(FigureA):
    def draw(self, img):
        draw = Draw(img)
        c1, c2, c3, = self.colors()
        # outline
        if self.outline:
            draw.polygon((*self.A(), *self.B(), *self.C(), *self.D(), *self.E(), *self.F()), self.pen(c))

        # cross lines
        for a, b in zip(self.ED, self.FA):
            draw.line((*a(), *b()), self.pen(c1))

        for a, b in zip(self.ED, self.BC):
            draw.line((*a(), *b()), self.pen(c2))

        for a, b in zip(self.CB, self.FA):
            draw.line((*a(), *b()), self.pen(c3))

        draw.flush()

class FigureC(FigureA):
    def draw(self, img):
        draw = Draw(img)
        c1, c2, c3, = self.colors()
        # outline
        if self.outline:
            draw.polygon((*self.A(), *self.B(), *self.C(), *self.D(), *self.E(), *self.F()), self.pen(c))

        for a, b in zip(self.rootE, self.FE):
            draw.line((*a(), *b()), self.pen(c1))

        for a, b in zip(self.rootE, self.DE):
            draw.line((*a(), *b()), self.pen(c1))

        for a, b in zip(self.rootC, self.DC):
            draw.line((*a(), *b()), self.pen(c2))

        for a, b in zip(self.rootC, self.BC):
            draw.line((*a(), *b()), self.pen(c2))

        for a, b in zip(self.rootA, self.FA):
            draw.line((*a(), *b()), self.pen(c3))

        for a, b in zip(self.rootA, self.BA):
            draw.line((*a(), *b()), self.pen(c3))

        # bold inner Y
        # draw.line((*self.root(), *self.F()), self.pen(c, 2))
        # draw.line((*self.root(), *self.D()), self.pen(c, 2))
        # draw.line((*self.root(), *self.B()), self.pen(c, 2))

        draw.flush()

def grid_points(cols, rows, u):
    dx = u * 2 * cos(pi / 6)
    dy = 3 * u / 2
    for i, j in product(range(cols), range(rows)):
        off = 0
        if j % 2 == 1:
            off = dx / 2
        yield dx * i + off, dy * j

args = parameters(WIDTH=700, HEIGHT=700)

all_colors = list(month_palette(args.month, args.p))
shuffle(all_colors)
bg, *colors = all_colors
p = PaletteRNG(colors)
canvas = Canvas(args.width, args.height, color=bg)

rows = 10
cols = 10
u = 70

w = 2
figs = [FigureA(p, w), FigureC(p, w), FigureB(p, w)]
for fig, (x, y) in zip(shuffle_cycle(figs), grid_points(cols, rows, u)):
    fig.config(u, False)
    fig.setup(x, y, 5)
    fig.draw(canvas.img)
canvas.save(args.out)
