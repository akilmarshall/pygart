from stroke import *
from color import *
from canvas import Canvas
from path import line
from util import info

from PIL import ImageDraw
from itertools import permutations
from random import choice


class Brick:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
    def _pos(self, x:int , y:int):
        return (x, y, x + self.width, y + self.height)
    def __call__(self, canvas, x:int, y:int, color):
        ImageDraw.Draw(canvas.img).rectangle(self._pos(x, y), fill=color)

def BrickRow(canvas, x, y, n, brick, palette):
    for i in range(n):
        xi = x + (i * brick.width)
        brick(canvas, xi, y, palette()) 

def BrickWall(canvas, x, y, n, m, brick, pallet):
    for i in range(m):
        yi = y + (i * brick.height)
        BrickRow(canvas, x + ((i%2) * (brick.width/2)), yi, n, brick, pallet) 

width, height, path = info()

canvas = Canvas(width, height)
a, b, c, d = choice(list(permutations([red, base00, base01, base02])))
p = CosinePalette(a, b, c, d)
brick = Brick(20, 10)
cols = 19
rows = 40

x = (width / 2) - (brick.width * cols / 2)
y = (height / 2) - (brick.height * rows / 2)
BrickWall(canvas, x, y, cols, rows, brick, p)

canvas.save(path)
