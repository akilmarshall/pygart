from pygart import info, Canvas, ComplexBox, PaletteRNG, getsu_set
from itertools import product

from random import randint
import numpy as np
from collections import defaultdict

class GOL:
    def __init__(self, data):
        self.data = data
        self.cols, self.rows = data.shape

    def neighbors(self, x, y):
        yield (x + 1) % self.cols, y
        yield (x + 1) % self.cols, (y + 1) % self.rows
        yield x, (y + 1) % self.rows
        yield (x - 1) % self.cols, (y + 1) % self.rows
        yield (x - 1) % self.cols, y
        yield (x - 1) % self.cols, (y - 1) % self.rows
        yield x, (y - 1) % self.rows
        yield (x + 1) % self.cols, (y - 1) % self.rows

    def neighbor_count(self, x, y):
        count = 0
        for h, k in self.neighbors(x, y):
            count += self.data[h][k]
        return int(count)

    def population_map(self):
        census = np.zeros((self.cols, self.rows), dtype=np.int8)
        for x, y in self._points():
            census[x][y] = self.neighbor_count(x, y)
        return census


    def alive(self, x, y):
        return self.data[x][y] == 1

    def step(self):
        census = self.population_map()
        for x, y in self._points():
            pop = census[x][y]
            if self.alive(x, y): 
                if pop < 2 or pop > 3:
                    self.data[x][y] = 0
            else:
                if pop == 3:
                    self.data[x][y] = 1

    def _points(self):
        for x, y in product(range(self.cols), range(self.rows)):
            yield x, y


p = PaletteRNG(list(getsu_set('july'))[4])
canvas = Canvas(*info(), color=p())

def stack(x, y, h, a, b, c, d, e, f, canvas):
    '''draw a stack of ComplexBox with h units. '''
    for i in range(h):
        ComplexBox(s, a(), b(), c(), d(), e(), f())(x, y - i * s // 2, canvas)

def floor(x, y, r, a, b, c, d, e, f, canvas):
    ComplexBox(r, a, b, c, d, e, f)(x, y, canvas)

class Frame:
    """A single snapshot of a city in growth ."""
    def __init__(self, rows:int, cols:int, radius:int, pallete):
        self.rows = rows
        self.cols = cols
        self.radius = radius
        self.pallete = pallete
        self.data = GOL(self.start())
        self.colors = self.make_colors()

    def start(self):
        data = np.zeros((self.cols, self.rows), dtype=np.int8)
        for x, y in self._points():
            data[x][y] = randint(0, 1)
        return data

    def make_colors(self):
        colors = {} 
        for x, y in self._points():
            colors[(x, y)] = [self._generate_params() for _ in range(4)]
        return colors


    def _generate_params(self):
        return self.pallete(), self.pallete(), self.pallete(), self.pallete(), self.pallete(), self.pallete()

    def step(self):
        """GOL step. """
        self.data.step()

    def _points(self):
        for x, y in product(range(self.cols), range(self.rows)):
            yield x, y
        
    def render(self, canvas):
        data = self.data.population_map()
        for x, y in self._points():
            n = data[x][y] 
            floors = self.colors[(x, y)][0:n]
            for i, params in enumerate(floors):
                a, b, c, d, e, f = params
                h = x * self.radius
                k = y * self.radius
                floor(h, k - i * self.radius // 2, self.radius, a, b, c, d, e, f, canvas)


steps = 200
frame = Frame(75, 75, 10, p)
for i in range(steps):
    frame.step()
    frame.render(canvas)
    canvas.save(f'frames/{i}.png')
