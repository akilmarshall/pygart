from itertools import product, chain
from math import cos, pi, sin
from random import random, shuffle

from PIL import ImageDraw

from pygart import Canvas, PaletteRNG, V, getsu_set, info

#w actions describe vertical translations or perhaps simple (1d) transforms.


class Kite:
    def __init__(self, n: int, r: int, pallet: PaletteRNG): 
        '''
        :n:         number of side of the polygon
        :r:         radius
        :pallet:    pallet to use
        '''
        self.n: int = n
        self.r: int = r
        self.pallet = pallet

    def setup(self, h: int, k: int, action: V): 
        '''
        :h:         x coord
        :k:         y coord
        '''
        theta = lambda x: 2 * pi * x / self.n
        self.primary = [V(h + self.r * cos(theta(i)), k + self.r * sin(theta(i))) for i in range(self.n)]
        self.secondary = [action + v for v in self.primary]

    def colors(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        while True:
            a = self.pallet()
            b = self.pallet()
            if a != b:
               return a, b 

    def draw(self, img):
        draw = ImageDraw.Draw(img)
        p1, p2 = self.colors()
        if random() > 0.5:
            draw.polygon([a() for a in self.primary], fill=p1)
            for a, b in zip(self.primary, self.secondary):
                draw.line((a(), b()), fill=p2, width=2)
            draw.polygon([a() for a in self.secondary], fill=p2)
        else:
            draw.polygon([a() for a in self.secondary], fill=p1)
            for a, b in zip(self.primary, self.secondary):
                draw.line((a(), b()), fill=p2, width=2)
            draw.polygon([a() for a in self.primary], fill=p2)


width, height, path = info()
N = [3, 5, 3, 6, 3, 5]
for i in range(6):
    colors = list(getsu_set('august'))[i]
    shuffle(colors)
    bg = colors.pop()
    p = PaletteRNG(colors)
    k = Kite(N[i], 30, p) 
    canvas = Canvas(width, height, path=f'{i}.png', color=bg)
    n, m = 3, 3
    xo = width / (n * 2)
    yo = height / (m * 2)
    dx = width / n
    dy = height / m
    for i, j in product(range(n), range(m)):
        x = int(i * dx + xo)
        y = int(j * dy + yo)
        k.setup(x, y, V(40, 15))
        k.draw(canvas.img)
    canvas.save()
