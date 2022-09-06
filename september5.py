from itertools import product
from math import cos, pi, sin

from aggdraw import Draw, Pen, Brush

from pygart import Canvas, PaletteRNG, V, getsu_set, info
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
    def __init__(self, pallete: PaletteRNG, s: int=6, width=4): 
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
        self.br = self.D + V(0, self.s * dy)


    def pen(self):
        # return Pen(self.p(), self.width)
        return None

    def brush(self):
        return Brush(self.p())

    def draw(self, img):
        draw = Draw(img)
        draw.polygon((*self.root(), *self.D(), *self.E(), *self.A()), self.brush(), self.pen())  # side face
        draw.polygon((*self.A(), *self.E(), *self.F(), *self.C()), self.brush(), self.pen())     # top face
        draw.polygon((*self.root(), *self.A(), *self.C(), *self.B()), self.brush(), self.pen())  # front face
        draw.line((*self.root(), *self.D()), self.pen())
        draw.line((*self.A(), *self.E()), self.pen())
        draw.line((*self.C(), *self.F()), self.pen())
        draw.line((*self.D(), *self.E()), self.pen())
        draw.line((*self.F(), *self.E()), self.pen())
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
        # self.c1 = c1
        # self.c2 = c2
        for fig in self.figs:
            fig.config(self.inner)

    def tile(self, img, fname='out.png'):
        for (i, j), fig in zip(product(range(self.s + 1), range(self.s + 1)), shuffle_cycle(self.figs)):
            i *= 2 * self.inner * sin(pi / 3)
            j *= 2 * self.inner * sin(pi / 3)
            fig.setup(i, j)
            x = random()
            if x < 0.35:
                fig.draw(img)
                # fig.draw(img, self.c1)
            # elif x < 0.6:
            #     continue
            # else:
            #     # fig.draw(img, self.c2)
            #     fig.draw(img)

        canvas.save(fname)


width, height, i = info()
i = int(i)
colors = list(getsu_set('september'))[i]
p = PaletteRNG(colors)
canvas = Canvas(width, height, color=p())
figs = [ContainerA(p, s=1), ContainerA(p, s=3), ContainerB(p, s=3)]
Tiling(figs, width, 20).tile(canvas.img,)
