from pygart import info, Canvas, draw, PaletteRNG, getsu_set
from itertools import product

from functools import partial
from random import randint


class FormA:
    def __init__(self, s:int):
        self.s = s

        self.sigma = self.s / 3
        self.X = self.s / 2, self.s / 2

    def apply(self, x, y, points):
        def sum_(A):
            ax, ay = A
            return ax + x, ay + y
        return list(map(sum_, points))

    def A(self):
        return [(0, 0), (self.s, 0), (2 * self.sigma, self.sigma), (self.sigma, self.sigma)] 

    def B(self):
        return [(2 * self.sigma, self.sigma), (2 * self.sigma, 2 * self.sigma), (self.s, self.s), (self.s, 0)] 

    def C(self):
        return [(0, self.s), (self.sigma, 2 * self.sigma), (2 * self.sigma, 2 * self.sigma), (self.s, self.s)] 

    def D(self):
        return [(0, 0), (self.sigma, self.sigma), (self.sigma, 2 * self.sigma), (0, self.s)] 

    def a(self):
        return [(self.sigma, self.sigma), (2 * self.sigma, self.sigma), self.X]

    def b(self):
        return [self.X, (2 * self.sigma, self.sigma), (2 * self.sigma, 2 * self.sigma)]

    def c(self):
        return [(self.sigma, self.sigma), self.X, (2 * self.sigma, 2 * self.sigma)]

    def d(self):
        return [(self.sigma, self.sigma), self.X, (self.sigma, 2 * self.sigma)]

    def __call__(self, x: int, y: int, A, B, canvas: Canvas):
        draw(self.apply(x, y, self.A()), A(), 0, 0, canvas) 
        draw(self.apply(x, y, self.B()), A(), 0, 0, canvas) 
        draw(self.apply(x, y, self.C()), A(), 0, 0, canvas) 
        draw(self.apply(x, y, self.D()), A(), 0, 0, canvas) 
        draw(self.apply(x, y, self.a()), B(), 0, 0, canvas) 
        draw(self.apply(x, y, self.b()), B(), 0, 0, canvas) 
        draw(self.apply(x, y, self.c()), B(), 0, 0, canvas) 
        draw(self.apply(x, y, self.d()), B(), 0, 0, canvas) 


class FormB:
    def __init__(self, s):
        self.s = s

        self.sigma = s / 2
        self.delta = s / 4

    def apply(self, x, y, points):
        def sum_(A):
            ax, ay = A
            return ax + x, ay + y
        return list(map(sum_, points))

    def shift(self, points):
        def apply(A):
            ax, ay = A
            return ax + self.sigma, ay
        return list(map(apply, points)) 

    def A(self):
        return [(0, 0), (self.sigma, 0), (self.delta, self.delta)]

    def B(self):
        return [(self.delta, self.delta), (self.sigma, 0), (self.sigma, self.s), (self.delta, 3 * self.delta)]

    def C(self):
        return [(0, self.s), (self.delta, 3 * self.delta), (self.sigma, self.s)]

    def D(self):
        return [(0, 0), (self.delta, self.delta), (self.delta, 3 * self.delta), (0, self.s)]

    def __call__(self, x: int, y: int, A, B, canvas: Canvas):
        draw(self.apply(x, y, self.A()), A(), 0, 0, canvas)
        draw(self.apply(x, y, self.B()), A(), 0, 0, canvas)
        draw(self.apply(x, y, self.C()), A(), 0, 0, canvas)
        draw(self.apply(x, y, self.D()), A(), 0, 0, canvas)
        draw(self.apply(x, y, self.shift(self.A())), B(), 0, 0, canvas)
        draw(self.apply(x, y, self.shift(self.B())), B(), 0, 0, canvas)
        draw(self.apply(x, y, self.shift(self.C())), B(), 0, 0, canvas)
        draw(self.apply(x, y, self.shift(self.D())), B(), 0, 0, canvas)


class FormC:
    def __init__(self, s):
        self.s = s

        self.sigma = s / 2
        self.delta = s / 4

    def apply(self, x, y, points):
        def sum_(A):
            ax, ay = A
            return ax + x, ay + y
        return list(map(sum_, points))

    def shift(self, points):
        def apply(A):
            ax, ay = A
            return ax, ay + self.sigma
        return list(map(apply, points)) 

    def A(self):
        return [(0, 0), (self.delta, self.delta), (0, self.sigma)]

    def B(self):
        return [(0, 0), (self.s, 0), (3 * self.delta, self.delta), (self.delta, self.delta)]

    def C(self):
        return [(3 * self.delta, self.delta), (self.s, 0), (self.s, self.sigma)]

    def D(self):
        return [(0, self.sigma), (self.delta, self.delta), (3 * self.delta, self.delta), (self.s, self.sigma)]

    def __call__(self, x: int, y: int, A, B, canvas: Canvas):
        draw(self.apply(x, y, self.A()), A(), 0, 0, canvas)
        draw(self.apply(x, y, self.B()), A(), 0, 0, canvas)
        draw(self.apply(x, y, self.C()), A(), 0, 0, canvas)
        draw(self.apply(x, y, self.D()), A(), 0, 0, canvas)
        draw(self.apply(x, y, self.shift(self.A())), B(), 0, 0, canvas)
        draw(self.apply(x, y, self.shift(self.B())), B(), 0, 0, canvas)
        draw(self.apply(x, y, self.shift(self.C())), B(), 0, 0, canvas)
        draw(self.apply(x, y, self.shift(self.D())), B(), 0, 0, canvas)

colors = list(getsu_set('august'))[5]
p = PaletteRNG(colors[0:2])
b = PaletteRNG(colors[2:])

print(colors[0:2])
print(colors[2:])

canvas = Canvas(*info())
s = 50
cols = 10
rows = 10

for i, j in product(range(cols), range(rows)):
    x = i * s
    y = j * s
    match randint(0, 2):
        case 0:
            FormA(s)(x, y, p, b, canvas)
        case 1:
            FormB(s)(x, y, p, b, canvas)
        case 2:
            FormC(s)(x, y, p, b, canvas)

canvas.save()
