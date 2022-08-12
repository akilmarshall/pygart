from pygart import info, Canvas, getsu_set, PaletteRNG
from itertools import product

from PIL import ImageDraw


class Form:
    def __init__(self, h: int, k: int, r: int, pallet: PaletteRNG): 
        self.r = r
        self.pallet = pallet

        self.setup(h, k)

    def setup(self, h: int, k: int): 
        self.u = (h, k)
        self.v = (h + self.r, k)
        self.w = (h, k + self.r)
        self.x = (h + self.r, k + self.r)
        half = self.r // 2
        self.M = (h + half, k + half)

    def draw_outline(self, img):
        draw = ImageDraw.Draw(img)
        draw.line([self.u, self.v], fill=self.pallet(), width=2)    # a
        draw.line([self.v, self.x], fill=self.pallet(), width=2)    # b
        draw.line([self.w, self.x], fill=self.pallet(), width=2)    # c
        draw.line([self.u, self.w], fill=self.pallet(), width=2)    # d

    def a(self, img):
        """Draw form a. """
        self.draw_outline(img)
        draw = ImageDraw.Draw(img)
        draw.line([self.w, self.v], fill=self.pallet(), width=2)    # e
        draw.line([self.M, self.x], fill=self.pallet(), width=2)    # f

    def b(self, img):
        """Draw form a. """
        self.draw_outline(img)
        draw = ImageDraw.Draw(img)
        draw.line([self.u, self.x], fill=self.pallet(), width=2)    # e
        draw.line([self.M, self.v], fill=self.pallet(), width=2)    # f


colors = list(getsu_set('august'))[5]
p = PaletteRNG(colors)
width, height, path = info()
canvas = Canvas(width, height, color=p())
s = 50
f = Form(0, 0, s, p)
f.a(canvas.img)

cols = width // s
rows = height // s 

for i, j in product(range(cols), range(rows)):
    x = i * s
    y = j * s
    f.setup(x, y)
    if (i + j) % 2 == 0:
        f.a(canvas.img)
    else:
        f.b(canvas.img)

canvas.save()
