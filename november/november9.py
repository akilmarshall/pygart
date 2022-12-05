from itertools import product
from math import cos, pi, sin

from aggdraw import Draw, Pen, Brush

from pygart import Canvas, PaletteRNG, V, parameters, month_palette, line, PaletteOrdered, ground_colors
from random import shuffle, choice, random

class Clifford:
    def __init__(self, a:float, b:float, c:float, d:float, x:float, y:float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
        self.origin = V(x, y)

        self.path = [self.origin]

    @property
    def n(self):
        return len(self.path)

    @property
    def point(self):
        x_, y_ = self.path[-1]()
        x = sin(self.a * y_) + self.c * cos(self.a * x_)
        y = sin(self.b * x_) + self.d * cos(self.b * y_)
        point = V(x, y)
        self.path.append(point)
        return self.origin + point


    def reset(self, x:float|None=None, y:float|None=None):
        if x:
            self._x = x
        if y:
            self._y = 0
        self.path = [(self._x, self._y)]

args = parameters(WIDTH=600, HEIGHT=600)
bg, colors = ground_colors(list(month_palette(args.month, args.p)))
shuffle(colors)
# bg, *colors = all_colors
p = PaletteRNG(colors)
canvas = Canvas(args.width, args.height, color=None)

p = 100000

clifford = Clifford(-34, 25, 2, 2, args.width / 2, args.height / 2)
path = []
pen = Pen(choice(colors), 1)
draw = Draw(canvas.img)

for _ in range(p):
    v, w = clifford.point()
    x, y = clifford.point()
    draw.line((v, w, x, y), pen)

# draw.line(path, Pen(choice(colors), 2))
draw.flush()
canvas.save(args.out)
