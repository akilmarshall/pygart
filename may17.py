from itertools import permutations, product
from random import choice

from PIL import ImageDraw

from canvas import Canvas
from color import CosinePalette, solarized
from util import info
from quadtree import Region


class Brick:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
    def _pos(self, x:int , y:int):
        return (x, y, x + self.width, y + self.height)
    def __call__(self, canvas, x:int, y:int, color):
        ImageDraw.Draw(canvas.img).rectangle(self._pos(x, y), fill=color)
'''

def BrickRow(canvas, x, y, n, brick, palette):
    for i in range(n):
        xi = x + (i * brick.width)
        brick(canvas, xi, y, palette()) 

def BrickWall(canvas, x, y, n, m, brick, pallet):
    for i in range(m):
        yi = y + (i * brick.height)
        BrickRow(canvas, x + ((i%2) * (brick.width/2)), yi, n, brick, pallet) 

'''

class Area:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def ideal_pattern(self, width:int, height:int):
        '''
        For the brick parameters compute an "ideal" brick pattern compute the positions of the upper left corner
        of the brick pattern over the Area
        '''
        cols = self.width // width
        rows = self.height // height
        pattern = []
        for x, y in product(range(cols), range(rows)):
                h = (width * x) + ((y % 2) * (width/2))
                k = (height * y)
                # h = (width * x)
                # k = (height * y) + ((x % 2) * (width/2))
                pattern.append((h, k))
        return pattern

width, height, path = info()
canvas = Canvas(width, height)

a, b, c, d = [solarized['red'], (130, 25, 10), solarized['base01'], solarized['base00']]

pallet = CosinePalette(a, b, c, d)
brick = Brick(30, 60)
region = Region(250, 250, 80, 40, 3/2)

area = Area(480, 480)
region(canvas)

canvas.save(path)
