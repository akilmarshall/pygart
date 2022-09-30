from itertools import product
from math import cos, pi, sin

from aggdraw import Draw, Brush

from pygart import Canvas, V, parameters, month_palette
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
    def __init__(self, colors, s: int=6, width=4): 
        '''
        :u:         unit length
        :s:         length ratio
        '''
        self.s = s
        self.colors = colors
        self.width = width

    def config(self, u, mode=True):
        self.u = u
        self.mode = mode

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

    def brush(self, c):
        return Brush(c)

    def scheme(self):
        if self.mode:
            return self.colors[0], self.colors[0], self.colors[1]
        return self.colors[0], self.colors[1], self.colors[0]


    def draw(self, img):
        draw = Draw(img)
        A, B, C = self.scheme()
        draw.polygon((*self.root(), *self.D(), *self.E(), *self.A()), self.brush(B), self.pen())  # side face
        draw.polygon((*self.A(), *self.E(), *self.F(), *self.C()), self.brush(A), self.pen())     # top face
        draw.polygon((*self.root(), *self.A(), *self.C(), *self.B()), self.brush(C), self.pen())  # front face
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

# width, height, out, i, unit_size = produce(scale=40)
args = parameters(WIDTH=700, HEIGHT=700)
colors = list(month_palette(args.month, args.p))
shuffle(colors)

canvas = Canvas(args.width, args.height, color=colors[0])
figA = ContainerB(colors[1:], s=2.5)
shuffle(colors)
figB = ContainerA(colors[1:], s=2.5)
flag = 0
COLS, ROWS = 8, 8
deltaX = args.width * 1.1 / COLS
deltaY = args.height * 1.1 / ROWS

for i, j in product(range(COLS), range(ROWS)):
    figB.config(20, flag % 3)
    x = i * deltaX + (deltaX / 2)
    y = j * deltaY + (deltaY / 2)
    figB.setup(x, y)
    figB.draw(canvas.img)
    flag += 1

flag = 1
for i, j in product(range(COLS), range(ROWS)):
    figA.config(20, flag % 3)
    x = i * deltaX
    y = j * deltaY
    figA.setup(x, y)
    figA.draw(canvas.img)
    flag += 1

canvas.save()
