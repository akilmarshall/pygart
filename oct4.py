from itertools import product, cycle
from math import cos, pi, sin

from aggdraw import Draw, Pen, Brush

from pygart import Canvas, PaletteRNG, V, parameters, month_palette, line, PaletteOrdered
from random import shuffle, choice, randint

def shuffle_cycle(lst):
    while True:
        for l in lst:
            yield l
        shuffle(lst)

def S(magnitude, theta):
    """Action. """
    return V(magnitude * cos(theta), magnitude * sin(theta))

class FigureA:
    def __init__(self, palette: PaletteRNG, w=4): 
        '''
        :u:         unit length
        '''
        self.p = palette
        self.p_ordered = PaletteOrdered(palette.colors)
        self.w = w

    def config(self, u, orientation, outline=True):
        self.u = u
        self.outline = outline
        self.orientation = orientation

    def setup(self, x, y, t=1): 
        """
        n points on the line segments, cross and inner
        """
        u = self.u
        root = self.root = V(x, y)
        self.A = root + S(t * u, pi / 6) 
        self.B = root + S(t * u, pi / 2)
        self.C = root + S(t * u, 5 * pi / 6)
        self.D = root + S(t * u, 7 * pi / 6)
        self.E = root + S(t * u, 3 * pi / 2)
        self.F = root + S(t * u, 11 * pi / 6) 

        self.Bi = self.B - V(0, u)
        self.Ei = self.E + V(0, u)

    def pen(self, c,):
        return Pen(c, self.w)

    def brush(self, c):
        return Brush(c)

    def colors(self):
        # c1, c2, c3, = (self.p_ordered(), self.p_ordered(), self.p_ordered())
        c1 = c2 = c3 = self.p()
        return c1, c2, c3

    def draw(self, img):
        draw = Draw(img)
        # c1, c2, c3, = self.colors()
        c = self.p()
        # outline
        if self.outline:
            draw.polygon((*self.A(), *self.B(), *self.C(), *self.D(), *self.E(), *self.F()), self.pen(c))
        match self.orientation:
            case 1:
                draw.polygon((*self.B(), *self.Bi(), *self.D(), *self.C()), self.brush(c))
            case 2:
                draw.polygon((*self.B(), *self.Bi(), *self.F(), *self.A()), self.brush(c))
            case 3:
                draw.polygon((*self.E(), *self.Ei(), *self.A(), *self.F()), self.brush(c))
            case 4:
                draw.polygon((*self.E(), *self.Ei(), *self.C(), *self.D()), self.brush(c))

        draw.flush()


def grid_points(cols, rows, u):
    dx = u * 2 * cos(pi / 6)
    dy = 3 * u / 2
    for i, j in product(range(cols), range(rows)):
        off = 0
        if j % 2 == 1:
            off = dx / 2
        yield dx * i + off, dy * j

args = parameters(WIDTH=775, HEIGHT=775)

all_colors = list(month_palette(args.month, args.p))
shuffle(all_colors)
bg, *colors = all_colors
p = PaletteRNG(colors)
canvas = Canvas(args.width, args.height, color=bg)

u = 50 
rows = 1 + (args.width // u)
cols = 1 + (args.height // u)

w = 3
figs = [FigureA(p, w)]
for fig, (x, y) in zip(shuffle_cycle(figs), grid_points(cols, rows, u)):
    fig.config(u, randint(1, 4), choice([True, False, False, False]))
    fig.setup(x, y)
    fig.draw(canvas.img)
canvas.save(args.out)
