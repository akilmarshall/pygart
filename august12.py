from pygart import info, Canvas, getsu_set, PaletteRNG, V
from itertools import product

from PIL import ImageDraw
from random import choice, random
from math import cos, sin, pi

# actions describe vertical translations or perhaps simple (1d) transforms.


class OO:
    def __init__(self,r: int, pallet: PaletteRNG, e: int = 2): 
        '''
        :r:         radius
        :pallet:    pallet to use
        :e:         inverse eccentricity parameter of the inner circle
        '''
        self.r: int = r
        self.pallet = pallet
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
        dashes = 9
        dash_radius = 2
        self.dash = []
        for i in range(dashes):
            theta = (pi) + (pi * i / dashes)
            p = lambda x: self.M + V(int(0.9 * self.r * cos(theta + x)), int(0.9 * self.r * sin(theta + x)))
            left = p(-dash_radius * pi / 180)
            right = p(dash_radius * pi / 180)
            self.dash.append((left, right))


    def colors(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        while True:
            a = self.pallet()
            b = self.pallet()
            if a != b:
               return a, b 

    def draw(self, img, r=None):
        draw = ImageDraw.Draw(img)
        p1, p2 = self.colors()
        draw.ellipse([self.a(), self.b()], p1, outline=p2, width=2)
        draw.ellipse([self.c(), self.d()], p1, outline=p2, width=2)
        for l, r in self.dash:
            draw.polygon((self.M(), l(), r()), fill=p1)



colors = list(getsu_set('august'))[4]
p = PaletteRNG(colors)
width, height, path = info()
canvas = Canvas(width, height, color=p())
s = 50
d = 30 
noise_radius = 5 

cols = width // s
rows = height // s 

objs = []
oo = OO(s - d, p)
objs.append(oo)

for i, j in product(range(cols), range(rows)):
    x = i * s + s // 2
    y = j * s + s // 2
    shape = choice(objs)
    theta = random()
    shape.e = choice([2, 2.5])
    shape.setup(x + noise_radius * cos(theta * 2 * pi), y + noise_radius * sin(theta * 2 * pi))
    shape.draw(canvas.img)

canvas.save()
