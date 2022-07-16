from pygart.util import info
from pygart.canvas import Canvas
from pygart.iso import ComplexBox
from pygart.color import PaletteRNG, getsu_set
from pygart.path import line

from PIL import ImageDraw
from random import randint, choice


class Building:

    def __init__(self, side, stories, n, m, A, B, C, T):
        self.side = side
        self.stories = stories
        self.n = n
        self.m = m
        self.A = A  # pallete for primary diamond
        self.B = B  # pallete for left
        self.C = C  # pallete for right
        self.T = T  # pallete for floor trim

    def __call__(self, x, y, canvas):
        for i in range(self.stories):
            h, k = x, y - i * self.side // 2
            unit = ComplexBox(
                    self.side,
                    self.A(),
                    self.B(),
                    self.C(),
                    None,
                    None,
                    None)
            unit(h, k, canvas, self.n, self.m)
            i_ = unit.i(h, k, self.n, self.m)
            trim = [
                    unit.apply(unit.o(h, k, self.n), 1),
                    unit.apply(i_, 1),
                    unit.apply(unit.u(h, k, self.m), 1),
                    ]
            ImageDraw.Draw(canvas.img).line(trim, fill=self.T(), width=2)
            wall = [i_, unit.apply(i_, 1)]
            ImageDraw.Draw(canvas.img).line(wall, fill=self.T(), width=2)


def row(x, y, n, building, canvas, gap=2):
    for i in range(n):
        h, k = x + i * building.side * gap, y + i * building.side * gap
        building(h, k, canvas)


def strip(building, points, canvas):
    for h, k in points:
        building.stories = randint(1, 5)
        building(h, k, canvas)


width, height, path = info()
canvas = Canvas(width, height)
gray = PaletteRNG([(128, 128, 128)])
side = 25
pad = 2 * side
Y = lambda : randint(pad, pad * 3) 
ax, ay = (pad, Y())
bx, by = (width - pad, Y())
p = PaletteRNG(choice(list(getsu_set('july'))))
building = Building(side, 0, 2, 1, p, p, p, p)
for j in range(4):
    strip(building, line((ax, ay + j * 2 * pad), (bx, by + j * 2 * pad), 10), canvas)
canvas.save(path)

