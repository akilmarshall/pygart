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


class Truck:
    def __init__(self, pallete: PaletteRNG, s: int=6): 
        '''
        :u:         unit length
        :s:         length ratio
        '''
        self.s = s
        self.p = pallete

    def config(self, u,):
        self.u = u

    def setup(self, x: int, y: int, d = 6): 
        u = self.u
        i = V(cos(pi / 6), 0) * u
        j = V(0, sin(pi / 6)) * u
        self.root = root = V(x, y)
        self._A = V(x, y - u)
        self._B = root - (i + j)
        self._C = self._B - V(0, u)
        self._D = root + self.s * (i - j)
        self._E = self._D + V(0, -u)
        self._F = self._E - (i + j)

        dy = V(0, u / d)
        self.A = root + dy
        self.B = self.A - (i + j)
        self.C = self.B + dy
        self.D = self.A + dy
        self.E = self.D + self.s * (i - j)
        self.F = self.E - dy
        self.G = self.F - (i + j)

        # self.H = self.D + dy
        self.I = self.D + i / 2 + 2 * dy


    def pen(self, c, w=2):
        return Pen(c, w)

    def brush(self, c):
        return Brush(c)

    def draw(self, img, load=False):
        draw = Draw(img)
        shuffle(self.p.colors)
        inner, outer, *_ = self.p.colors
        if load:
            draw.polygon((*self.root(), *self._D(), *self._E(), *self._A()), self.brush(inner), self.pen(outer))  # side face
            draw.polygon((*self._A(), *self._E(), *self._F(), *self._C()), self.brush(inner), self.pen(outer))     # top face
            draw.polygon((*self.root(), *self._A(), *self._C(), *self._B()), self.brush(inner), self.pen(outer))  # front face
            draw.line((*self.root(), *self._D()), self.pen(outer))
            draw.line((*self._A(), *self._E()), self.pen(outer))
            draw.line((*self._C(), *self._F()), self.pen(outer))
            draw.line((*self._D(), *self._E()), self.pen(outer))
            draw.line((*self._F(), *self._E()), self.pen(outer))

        # bed platform
        draw.polygon((*self.A(), *self.B(), *self.C(), *self.D(), *self.E(), *self.F()), self.brush(inner), self.pen(outer))
        # platform top
        draw.polygon((*self.A(), *self.B(), *self.G(), *self.F()), self.brush(inner))
        # platform outline
        draw.line((*self.F(), *self.G()), self.pen(outer))
        draw.line((*self.B(), *self.G()), self.pen(outer))

        # front wheel
        draw.ellipse((*self.D(), *self.I(),), self.brush(inner), self.pen(outer))

        draw.flush()


out = 'out.png'
width, height, i = info()

i = int(i)
colors = list(getsu_set('september'))[i]
p = PaletteRNG(colors)
canvas = Canvas(width, height, color=p())
truck = Truck(p, s=2)
truck.config(50)
truck.setup(width // 2, height // 2)
truck.draw(canvas.img)
canvas.save(out)
