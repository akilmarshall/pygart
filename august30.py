from pygart import info, Canvas, getsu_set, V, PaletteRNG
from itertools import product, cycle

from PIL import ImageDraw


class FigureA:
    def __init__(self, p: PaletteRNG): 
        '''
        :u:         unit length
        '''
        self.p = p
    def config(self, s: int):
        self.s = s

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
        return {'fill':self.p(), 'outline':self.p(), 'width':0}

    def draw(self, img):
        d = ImageDraw.Draw(img)
        d.polygon((self.J(), self.A(), self.I()), **self.args())
        d.polygon((self.C(), self.E(), self.G()), **self.args())
        d.polygon((self.A(), self.D(), self.C(), self.G(), self.F(), self.I()), **self.args())
        d.polygon((self.I(), self.F(), self.G(), self.H()), **self.args())
        d.polygon((self.A(), self.B(), self.C(), self.D()), **self.args())

class FigureB(FigureA):
    def draw(self, img):
        d = ImageDraw.Draw(img)
        d.polygon((self.J(), self.A(), self.I()), **self.args())
        d.polygon((self.A(), self.B(), self.C()), **self.args())
        d.polygon((self.C(), self.E(), self.G()), **self.args())
        d.polygon((self.G(), self.H(), self.I()), **self.args())
        d.polygon((self.A(), self.C(), self.G(), self.I()), **self.args())


class Tiling:
    """Square tiling with square tiles.  """
    def __init__(self, figs: list[FigureA], outer, inner):
        self.figs = figs
        self.outer = outer
        self.inner = inner
        self.s = self.outer // self.inner
        for fig in self.figs:
            fig.config(self.inner)

    def tile(self, img, fname='out.png'):
        for (i, j), fig in zip(product(range(self.s + 1), range(self.s + 1)), cycle(self.figs)):
            i *= self.inner
            j *= self.inner
            fig.setup(i, j)
            fig.draw(img)

        canvas.save(fname)


p = PaletteRNG(list(getsu_set('august'))[0])
width, height, path = info()
canvas = Canvas(width, height)
figs = [FigureA(p), FigureB(p)]
Tiling(figs, width, 50).tile(canvas.img)
