from pygart import info, Canvas, ComplexBox, PaletteRNG, getsu_set
from itertools import product

from random import randint
import numpy as np
from collections import defaultdict

# scales used: 20, 50, 100, 200
# col, row = 6 * 5, 5 * 5

# s = 200
# r = -s // 2
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
        self.data = defaultdict(list)


    def _generate_params(self):
        return self.pallete(), self.pallete(), self.pallete(), self.pallete(), self.pallete(), self.pallete()

    def _random_position(self):
        return randint(0, self.cols - 1), randint(0, self.rows - 1)

    def step(self):
        """Grow a random position by 1 story. """
        x, y = self._random_position()
        self.data[(x, y)].append(self._generate_params())

    def _points(self):
        for x, y in product(range(self.cols), range(self.rows)):
            yield x, y
        
    def render(self, canvas):
        for x, y in self._points():
            for i, params in  enumerate(self.data[(x, y)]):
                a, b, c, d, e, f = params
                h = x * self.radius
                k = y * self.radius
                floor(h, k - i * self.radius // 2, self.radius, a, b, c, d, e, f, canvas)


steps = 50
frame = Frame(15, 15, 50, p)
for i in range(steps):
    frame.step()
    frame.render(canvas)
    canvas.save(f'frames/{i}.png')
