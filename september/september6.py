from itertools import product
from math import cos, pi, sin

from aggdraw import Draw, Pen, Brush

from pygart import Canvas, PaletteRNG, V, getsu_set, produce, parameters, month_palette
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
    def __init__(self, pallete: PaletteRNG, s: int=6): 
        '''
        :u:         unit length
        :s:         length ratio
        '''
        self.s = s
        self.p = pallete

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


    def pen(self, c, w=2):
        return Pen(c, w)

    def brush(self, c):
        return Brush(c)

    def draw(self, img):
        draw = Draw(img)
        shuffle(self.p.colors)
        inner, outer, *_ = self.p.colors
        draw.polygon((*self.root(), *self.D(), *self.E(), *self.A()), self.brush(inner), self.pen(outer))  # side face
        draw.polygon((*self.A(), *self.E(), *self.F(), *self.C()), self.brush(inner), self.pen(outer))     # top face
        draw.polygon((*self.root(), *self.A(), *self.C(), *self.B()), self.brush(inner), self.pen(outer))  # front face
        draw.line((*self.root(), *self.D()), self.pen(outer))
        draw.line((*self.A(), *self.E()), self.pen(outer))
        draw.line((*self.C(), *self.F()), self.pen(outer))
        draw.line((*self.D(), *self.E()), self.pen(outer))
        draw.line((*self.F(), *self.E()), self.pen(outer))
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
            x = random()
            if x < 0.5:
                fig.draw(img)

        canvas.save(fname)

# width, height, out, i, unit_size = produce(scale=60, unit_size=20)
args = parameters(WIDTH=700, HEIGHT=700)
colors = list(month_palette(args.month, args.p))
unit_size = 20
out = args.out


# colors = list(getsu_set('september'))[i]
p = PaletteRNG(colors)
canvas = Canvas(args.width, args.height, color=p())
figs = [ContainerA(p, s=1), ContainerA(p, s=3), ContainerB(p, s=3)]
Tiling(figs, args.width, unit_size).tile(canvas.img, fname=out)
