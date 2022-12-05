from itertools import product
from math import cos, pi, sin

from aggdraw import Draw, Pen, Brush

from pygart import Canvas, PaletteRNG, V, getsu_set, produce
from random import shuffle, random

def shuffle_cycle(lst):
    while True:
        for l in lst:
            yield l
        shuffle(lst)


def S(magnitude, theta):
    """Action. """
    return V(magnitude * cos(theta), magnitude * sin(theta))


class ContainerA:
    def __init__(self, pallete: PaletteRNG, s: float=6, width=2): 
        '''
        :u:         unit length
        :s:         length ratio
        '''
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
        self.G = self.F + V(0, u)
        self.br = self.D + V(0, self.s * dy)

    def pen(self):
        return Pen(self.p(), self.width)

    def draw(self, img, c):
        pen = Pen(c, self.width)
        draw = Draw(img)
        draw.line((*self.root(), *self.D()), pen)
        draw.line((*self.A(), *self.root()), pen)
        draw.line((*self.B(), *self.root()), pen)
        draw.line((*self.A(), *self.E()), pen)
        draw.line((*self.C(), *self.F()), pen)
        draw.line((*self.D(), *self.E()), pen)
        draw.line((*self.F(), *self.E()), pen)
        draw.line((*self.B(), *self.G()), pen)
        draw.line((*self.F(), *self.G()), pen)
        draw.line((*self.D(), *self.G()), pen)
        draw.line((*self.A(), *self.C()), pen)
        draw.line((*self.B(), *self.C()), pen)
        draw.flush()


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
        self.G = self.F + V(0, u)
        self.br = self.D + V(0, self.s * dy)


class Tiling:
    """Square tiling with square tiles.  """
    def __init__(self, figs: list[ContainerA], outer, inner, c1, c2):
        self.figs = figs
        self.outer = outer
        self.inner = inner
        self.s = self.outer // self.inner
        self.c1 = c1
        self.c2 = c2
        for fig in self.figs:
            fig.config(self.inner)

    def tile(self, img, fname='out.png'):
        for (i, j), fig in zip(product(range(self.s + 1), range(self.s + 1)), shuffle_cycle(self.figs)):
            i *= 2 * self.inner * sin(pi / 3)
            j *= 2 * self.inner * sin(pi / 3)
            fig.setup(i, j)
            x = random()
            if x < 0.1:
                fig.draw(img, self.c1)
            elif x < 0.4:
                fig.draw(img, self.c2)

        canvas.save(fname)


width, height, out, i, unit_size = produce(scale=60, unit_size=20)

colors = list(getsu_set('september'))[i]
shuffle(colors)
c1, c2, c3, *_ = colors
p = PaletteRNG(colors)
canvas = Canvas(width, height, color=c1)
figs = [ContainerA(p, s=1.5), ContainerB(p, s=1.5), ContainerA(p, s=4), ContainerB(p, s=2)]
Tiling(figs, width, unit_size, c2, c3).tile(canvas.img, fname=out)
