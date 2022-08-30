from pygart import info, Canvas, getsu_set, V, PaletteRNG
from itertools import product, cycle

from PIL import ImageDraw
from random import  shuffle


class FigureA:
    def __init__(self, s: int, p: PaletteRNG, img): 
        '''
        :u:         unit length
        '''
        self.s = s
        self.p = p
        self.d = ImageDraw.Draw(img)

    def setup(self, x: int, y: int): 
        self.root = root = V(x, y)
        xact = V(self.s / 4, 0)
        yact = V(0, self.s / 4)
        self.A = root - 2 * yact
        self.B = self.A + 2 * xact
        self.C = self.B + yact
        self.D = root - yact
        self.E = self.C + 3 * yact
        self.F = root + yact
        self.G = self.F + yact
        self.H = self.G - 2 * xact
        self.I = self.H - yact
        self.J = self.A - 2 * xact
    def args(self):
        return {'fill':self.p(), 'outline':self.p(), 'width':2}

    def draw(self):
        self.d.polygon((self.J(), self.A(), self.I()), **self.args())
        self.d.polygon((self.C(), self.E(), self.G()), **self.args())
        self.d.polygon((self.A(), self.D(), self.C(), self.G(), self.F(), self.I()), **self.args())
        self.d.polygon((self.I(), self.F(), self.G(), self.H()), **self.args())
        self.d.polygon((self.A(), self.B(), self.C(), self.D()), **self.args())

class FigureB(FigureA):
    def draw(self):
        self.d.polygon((self.J(), self.A(), self.I()), **self.args())
        self.d.polygon((self.A(), self.B(), self.C()), **self.args())
        self.d.polygon((self.C(), self.E(), self.G()), **self.args())
        self.d.polygon((self.G(), self.H(), self.I()), **self.args())
        self.d.polygon((self.A(), self.C(), self.G(), self.I()), **self.args())



p = PaletteRNG(list(getsu_set('august'))[5])
width, height, path = info()
canvas = Canvas(width, height,)
s = 50
cols = width // s
rows = height // s
figs = [FigureA(s, p, canvas.img), FigureB(s, p, canvas.img)]
for (i, j), fig in zip(product(range(cols + 1), range(rows + 1)), cycle(figs)):
    i *= s
    j *= s
    fig.setup(i, j)
    fig.draw()

canvas.save()
