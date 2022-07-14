from functools import partial
from random import randint

from PIL import ImageDraw
import numpy as np
from scipy.stats import beta

from pygart.canvas import Canvas
from pygart.color import RGBA, solarized
from pygart.util import info


C = [solarized['red'], solarized['base03']]

class Characteristic:
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        fx = self.f(x)
        return max(0, fx)


# change the argument order for use with partial
def _beta_helper(a, b, x): return beta.pdf(x, a, b)
def alphabeta(a, b): return partial(_beta_helper, a, b)


class Stroke:
    def __init__(self, path, c, r):
        self.path = path
        self.c = c
        self.r = r

    def __call__(self, canvas, color=RGBA(solarized['base03'])):
        draw = ImageDraw.Draw(canvas.img)
        n = len(self.path)
        for i, (x, y) in enumerate(self.path):
            r = self.r * self.c(i / n)
            a, b = x - r, y - r
            c, d = x + r, y + r
            draw.ellipse((a, b, c, d), fill=color)


def background(width, height, step, r, fname):
    canvas = Canvas(width, height)
    l = height * 3 / 5
    ys = [(7 * height + 5 * l * i) / 35 for i in range(7)]
    a = width / 5
    b = 4 * width / 5
    def path(i): return [(x, ys[i]) for x in np.arange(a, b, step)]

    def x(): return randint(1, 5)
    for i in range(7):
        beta = Characteristic(alphabeta(x(), x()))
        Stroke(path(i), beta, r)(canvas, RGBA(C[i % 2]))
    canvas.save(fname)


width, height, path = info()
width = int(width)
height = int(height)
background(width, height, 20, 5, path)
