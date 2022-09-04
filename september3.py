from itertools import product
from math import cos, pi, sin

from PIL import ImageDraw

from pygart import Canvas, PaletteRNG, V, getsu_set, info
from random import shuffle

def shuffle_cycle(lst):
    while True:
        for l in lst:
            yield l
        shuffle(lst)


def S(magnitude, theta):
    """Action. """
    return V(magnitude * cos(theta), magnitude * sin(theta))


class ContainerA:
    def __init__(self, pallete: PaletteRNG, s: int=6, width=4): 
        '''
        :u:         unit length
        :s:         length ratio
        '''
        # self.u = u
        self.s = s
        self.p = pallete
        self.width = width

    def config(self, u,):
        self.u = u

    def setup(self, x: int, y: int): 
        u = self.u
        dx = u * cos(pi / 6)
        dy = u * sin(pi / 6)
        self.root = V(x, y)
        self.A = V(x, y - u)
        self.B = self.root + V(-dx, -dy)
        self.C = self.B + V(0, -u)
        self.D = self.root + V(self.s * dx, -self.s * dy)
        self.E = self.D + V(0, -u)
        self.F = self.E + V(-dx, -dy)
        self.br = self.D + V(0, self.s * dy)

    def args(self):
        return {'fill':self.p(), 'outline':self.p(), 'width':self.width}

    def args2(self):
        return {'fill':self.p(), 'width':self.width}

    def draw(self, img):
        draw = ImageDraw.Draw(img)
        draw.polygon((self.root(), self.D(), self.E(), self.A()), **self.args())  # side face
        draw.polygon((self.A(), self.E(), self.F(), self.C()), **self.args())     # top face
        draw.polygon((self.root(), self.A(), self.C(), self.B()), **self.args())  # front face
        draw.line((self.root(), self.D()), **self.args2())
        draw.line((self.A(), self.E()), **self.args2())
        draw.line((self.C(), self.F()), **self.args2())
        draw.line((self.D(), self.E()), **self.args2())
        draw.line((self.F(), self.E()), **self.args2())



class ContainerB(ContainerA):
    def setup(self, x: int, y: int): 
        u = self.u
        dx = u * cos(pi / 6)
        dy = u * sin(pi / 6)
        self.root = V(x, y)
        self.A = V(x, y - u)
        self.B = self.root + V(dx, -dy)
        self.C = self.B + V(0, -u)
        self.D = self.root + V(-self.s * dx, -self.s * dy)
        self.E = self.D + V(0, -u)
        self.F = self.E + V(dx, -dy)
        self.br = self.D + V(0, self.s * dy)


class Tiling:
    """Square tiling with square tiles.  """
    def __init__(self, figs: list[ContainerA], outer, inner):
        self.figs = figs
        self.outer = outer
        self.inner = inner
        self.s = self.outer // self.inner
        for fig in self.figs:
            fig.config(self.inner)

    def tile(self, img, fname='out.png'):
        for (i, j), fig in zip(product(range(self.s + 1), range(self.s + 1)), shuffle_cycle(self.figs)):
            i *= 2 * self.inner * sin(pi / 3)
            j *= 2 * self.inner * sin(pi / 3)
            fig.setup(i, j)
            fig.draw(img)

        canvas.save(fname)


width, height, i = info()
i = int(i)
colors = list(getsu_set('september'))[i]
p = PaletteRNG(colors)
canvas = Canvas(width, height, color=p())
figs = [ContainerA(p, s=1), ContainerA(p, s=3), ContainerB(p, s=2)]
Tiling(figs, width, 40).tile(canvas.img,)
