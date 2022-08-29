from pygart import info, Canvas, getsu_set, V
from itertools import product, cycle

from PIL import ImageDraw
from random import  shuffle


class FigureA:
    def __init__(self, s: int, colors): 
        '''
        :u:         unit length
        '''
        self.s = s
        self.c = colors

    def setup(self, x: int, y: int): 
        self.root = root = V(x, y)
        xaction = V(self.s / 2, 0)
        yaction = V(0, self.s / 2)
        self.A = root - xaction - yaction
        self.B = root - yaction
        self.C = root - yaction + xaction
        self.D = root + xaction
        self.E = root + xaction + yaction
        self.F = root + yaction
        self.G = root - xaction + yaction
        self.H = root - xaction

    def colors(self):
        yield self.c[0]  # color a
        yield self.c[1]  # color b
        yield self.c[2]  # color c

    def draw(self, img):
        c1, c2, *_ = self.colors()
        draw = ImageDraw.Draw(img)
        draw.polygon((self.A(), self.B(), self.H()), fill=c1)
        draw.polygon((self.B(), self.C(), self.D(), self.F(), self.G(), self.H()), fill=c2)
        draw.polygon((self.D(), self.E(), self.F()), fill=c1)

class FigureB(FigureA):
    def draw(self, img):
        c1, c2, *_ = self.colors()
        draw = ImageDraw.Draw(img)
        draw.polygon((self.H(), self.F(), self.G()), fill=c1)
        draw.polygon((self.A(), self.B(), self.D(), self.E(), self.F(), self.H()), fill=c2)
        draw.polygon((self.B(), self.C(), self.D()), fill=c1)

class FigureC(FigureA):
    def draw(self, img):
        c1, c2, c3 = self.colors()
        draw = ImageDraw.Draw(img)
        draw.polygon((self.A(), self.B(), self.H()), fill=c1)
        draw.polygon((self.B(), self.root(), self.G(), self.H()), fill=c2)
        draw.polygon((self.root(), self.E(), self.G()), fill=c1)
        draw.polygon((self.B(), self.D(), self.E(), self.root()), fill=c3)
        draw.polygon((self.B(), self.C(), self.D()), fill=c1)

class FigureD(FigureA):
    def draw(self, img):
        c1, c2, c3 = self.colors()
        draw = ImageDraw.Draw(img)
        draw.polygon((self.H(), self.F(), self.G()), fill=c1)
        draw.polygon((self.A(), self.root(), self.F(), self.H()), fill=c2)
        draw.polygon((self.A(), self.root(), self.C()), fill=c1)
        draw.polygon((self.C(), self.D(), self.F(), self.root()), fill=c3)
        draw.polygon((self.D(), self.E(), self.F()), fill=c1)


p = list(getsu_set('august'))[5]
width, height, path = info()
canvas = Canvas(width, height,)
s = 50
cols = width // s
rows = height // s
shuffle(p)
figs = [FigureC(s, p), FigureA(s, p)]
for (i, j), fig in zip(product(range(cols + 1), range(rows + 1)), cycle(figs)):
    i *= s
    j *= s
    fig.setup(i, j)
    fig.draw(canvas.img)

canvas.save()
