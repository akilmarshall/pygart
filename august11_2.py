from pygart import info, Canvas, getsu_set, PaletteRNG
from itertools import product

from PIL import ImageDraw
from random import choice, random
from math import cos, sin, pi

# actions describe vertical translations or perhaps simple (1d) transforms.

class V2:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def v(self) -> tuple[int, int]:
        return self.x, self.y

    def __add__(self, other):
        return V2(self.x + other.x, self.y + other.y)

    def __call__(self):
        return self.v()



class Cylinder:
    def __init__(self, h: int, k: int, r: int, pallet: PaletteRNG, e: int = 2): 
        '''
        :h:         x coord
        :k:         y coord
        :r:         radius
        :pallet:    pallet to use
        :e:         inverse eccentricity parameter
        '''
        self.r: int = r
        self.pallet = pallet
        self.e = e

        self.setup(h, k)

    def setup(self, h: int, k: int): 
        q = self.r // self.e
        action = V2(0, q)
        self.M = V2(h, k)
        self.N = self.M + action
        self.a = V2(h - self.r, k - q)
        self.b = V2(h + self.r, k + q)
        self.c = self.a + action
        self.d = self.b + action
        self.l = self.M + V2(-self.r, 0)
        self.ru = self.M + V2(self.r, q)

    def colors(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        while True:
            a = self.pallet()
            b = self.pallet()
            if a != b:
               return a, b 

    def draw(self, img):
        draw = ImageDraw.Draw(img)
        p1, p2 = self.colors()
        draw.ellipse([self.c.v(), self.d.v()], p1, outline=p2, width=2)
        draw.rectangle((self.l.v(), self.ru.v()), p1)
        draw.ellipse([self.a.v(), self.b.v()], p1, outline=p2, width=2)
        draw.line([self.c.v(), (self.c + V2(0, self.r // self.e)).v()], fill=p2, width=2)
        draw.line([self.b.v(), (self.b + V2(0, -self.r // self.e)).v()], fill=p2, width=2)


class TriangleA:
    def __init__(self, h: int, k: int, r: int, pallet: PaletteRNG): 
        '''
        :h:         x coord
        :k:         y coord
        :r:         radius 
        :pallet:    pallet to use
        '''
        self.r: int = r
        self.pallet = pallet

        self.setup(h, k)

    def setup(self, h: int, k: int): 
        s = self.r // 2
        self.M = V2(h, k)
        self.a = self.M + V2(0, -s)
        self.b = self.M + V2(-self.r, s)
        self.c = self.M + V2(self.r, s)
        self.d = self.c + V2(0, s)

    def colors(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        while True:
            a = self.pallet()
            b = self.pallet()
            if a != b:
               return a, b 

    def draw(self, img):
        draw = ImageDraw.Draw(img)
        p1, p2 = self.colors()
        draw.line([self.a.v(), self.b.v()], fill=p2, width=2)
        draw.line([self.a.v(), self.c.v()], fill=p2, width=2)
        draw.rectangle((self.b.v(), self.d.v()), fill=p1, outline=p2, width=2)


class TriangleB:
    def __init__(self, h: int, k: int, r: int, pallet: PaletteRNG): 
        '''
        :h:         x coord
        :k:         y coord
        :r:         radius 
        :pallet:    pallet to use
        '''
        self.r: int = r
        self.pallet = pallet

        self.setup(h, k)

    def setup(self, h: int, k: int): 
        s = self.r // 2
        self.M = V2(h, k)
        self.a = self.M + V2(-self.r, 0)
        self.b = self.M + V2(self.r, 0)
        self.c = self.M + V2(0, self.r)
        action = V2(0, s)
        self.d = self.a + action
        self.e = self.b + action
        self.f = self.c + action

    def colors(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        while True:
            a = self.pallet()
            b = self.pallet()
            if a != b:
               return a, b 

    def draw(self, img):
        draw = ImageDraw.Draw(img)
        p1, p2 = self.colors()
        draw.polygon((self.a(), self.c(), self.c(), self.b(), self.e(), self.f(), self.d(), self.a()), fill=p1)  # color background
        draw.polygon((self.a(), self.b(), self.c()), fill=p1, outline=p2, width=2)
        draw.line([self.a(), self.d()], fill=p2, width=2)
        draw.line([self.c(), self.f()], fill=p2, width=2)
        draw.line([self.b(), self.e()], fill=p2, width=2)
        draw.line([self.d(), self.f()], fill=p2, width=2)
        draw.line([self.f(), self.e()], fill=p2, width=2)


class TriangleC:
    def __init__(self, h: int, k: int, r: int, pallet: PaletteRNG): 
        '''
        :h:         x coord
        :k:         y coord
        :r:         radius 
        :pallet:    pallet to use
        '''
        self.r: int = r
        self.pallet = pallet

        self.setup(h, k)

    def setup(self, h: int, k: int): 
        s = self.r // 2
        self.M = V2(h, k)
        self.a = self.M + V2(-self.r, 0)
        self.b = self.M + V2(self.r, 0)
        self.c = self.M + V2(0, -self.r)
        action = V2(0, -s)
        self.d = self.a + action
        self.e = self.b + action
        self.f = self.c + action

    def colors(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        while True:
            a = self.pallet()
            b = self.pallet()
            if a != b:
               return a, b 

    def draw(self, img):
        draw = ImageDraw.Draw(img)
        p1, p2 = self.colors()
        draw.polygon((self.a(), self.c(), self.c(), self.b(), self.e(), self.f(), self.d(), self.a()), fill=p1)  # color background
        draw.polygon((self.a(), self.b(), self.c()), fill=p1, outline=p2, width=2)
        draw.line([self.a(), self.d()], fill=p2, width=2)
        draw.line([self.c(), self.f()], fill=p2, width=2)
        draw.line([self.b(), self.e()], fill=p2, width=2)
        draw.line([self.d(), self.f()], fill=p2, width=2)
        draw.line([self.f(), self.e()], fill=p2, width=2)


class Cube:
    def __init__(self, h: int, k: int, s: int, pallet: PaletteRNG): 
        '''
        :h:         x coord
        :k:         y coord
        :r:         side length 
        :pallet:    pallet to use
        '''
        self.s: int = s
        self.pallet = pallet

        self.setup(h, k)

    def setup(self, h: int, k: int): 
        M = V2(h, k)
        r = self.s // 2
        self.a = M + V2(-r, 0) 
        self.b = M + V2(0, -r) 
        self.c = M + V2(r, 0) 
        self.d = M + V2(0, r) 
        action = V2(0, r)
        self.e = self.a + action
        self.f = self.d + action
        self.g = self.c + action

    def colors(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        while True:
            a = self.pallet()
            b = self.pallet()
            if a != b:
               return a, b 

    def draw(self, img):
        draw = ImageDraw.Draw(img)
        p1, p2 = self.colors()
        draw.polygon((self.a(), self.d(), self.c(), self.g(), self.f(), self.e()), fill=p1)  # color background
        draw.polygon((self.a(), self.b(), self.c(), self.d()), fill=p1, outline=p2, width=2)
        draw.line([self.a(), self.e()], fill=p2, width=2)
        draw.line([self.d(), self.f()], fill=p2, width=2)
        draw.line([self.c(), self.g()], fill=p2, width=2)
        draw.line([self.e(), self.f()], fill=p2, width=2)
        draw.line([self.f(), self.g()], fill=p2, width=2)


colors = list(getsu_set('august'))[0]
p = PaletteRNG(colors)
width, height, path = info()
canvas = Canvas(width, height, color=p())
s = 50
d = 25
noise_radius = 20

cols = width // s
rows = height // s 

objs = []
objs.append(Cylinder(0, 0, s - d, p, e=1.5))
objs.append(TriangleA(0, 0, s - d, p))
objs.append(TriangleB(0, 0, s - d, p))
objs.append(TriangleC(0, 0, s - d, p))
objs.append(Cube(0, 0, s - d, p))

for i, j in product(range(cols), range(rows)):
    x = i * s + s // 2
    y = j * s + s // 2
    shape = choice(objs)
    theta = random()
    shape.setup(x + noise_radius * cos(theta * 2 * pi), y + noise_radius * sin(theta * 2 * pi))
    shape.draw(canvas.img)

canvas.save()
