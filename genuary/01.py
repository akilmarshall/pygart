from math import sin, pi
from pygart import Canvas, ComplexBox, getsu_set, PaletteRNG, RGBA
from pygart import parameters, month_palette, ground_colors, V
# from PIL import ImageDraw
from aggdraw import Draw, Pen, Brush
from random import choice
from math import sin, cos
from pathlib import Path
from os import rmdir, remove


class OO:
    def __init__(self,r: int, c1, c2, bg, e: int = 2): 
        '''
        :r:         radius
        :e:         inverse eccentricity parameter of the inner circle
        '''
        self.r: int = r
        self.c1 = c1
        self.c2 = c2
        self.bg = bg
        self.e = e

    def setup(self, h: int, k: int): 
        '''
        :h:         x coord
        :k:         y coord
        '''
        self.M = V(h, k)
        self.a = self.M + V(-self.r, -self.r)
        self.b = self.M + V(self.r, self.r)
        self.c = self.a + V(0, self.r // self.e)
        self.d = self.b + V(0, -self.r // self.e)
        dashes = 11
        dash_radius = 2
        self.dash = []
        for i in range(dashes):
            theta = (pi) + (pi * i / dashes)
            p = lambda x: self.M + V(int(0.9 * self.r * cos(theta + x)), int(0.9 * self.r * sin(theta + x)))
            left = p(-dash_radius * pi / 180)
            right = p(dash_radius * pi / 180)
            self.dash.append((left, right))

    def pen(self, c, w=4,):
        return Pen(c, w)

    def draw(self, draw):
        # p1, p2 = self.colors()
        draw.ellipse((*self.c(), *self.d()), self.pen(self.c1))
        draw.ellipse((*self.a(), *self.b()), self.pen(self.c2))
        for l, r in self.dash:
            draw.polygon((*self.M(), *l(), *r()), self.pen(self.bg, w=2))

args = parameters(WIDTH=600, HEIGHT=600)
bg, colors = ground_colors(list(month_palette(args.month, args.p)))
pen = Pen(choice(colors), 1)
# canvas = Canvas(args.width, args.height, color=bg)

obj = OO(40, choice(colors), choice(colors), bg)

frame_path = Path('frames')
if frame_path.is_dir():
    for f in frame_path.iterdir():
    # delete, make anew
        remove(f)
    rmdir(frame_path)
    frame_path.mkdir()
else:
    frame_path.mkdir()

path = []
n = 300
r = 150
for i in range(n):
    canvas = Canvas(args.width, args.height, color=bg)
    draw = Draw(canvas.img)
    theta = 2 * pi * i / n 
    x = int(r * cos(theta)) + args.width // 2
    y = int(r * sin(theta)) + args.height // 2
    obj.setup(x, y)
    obj.draw(draw)
    draw.flush()
    canvas.save(frame_path / f'{i}.png')
