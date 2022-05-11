from stroke import *
from canvas import Canvas
from random import random, choice
import numpy as np
from numpy import linspace
from color import *
from math import pi
from util import info


class CosinePalette:
    def __init__(self, a, b, c, d):
        self.a = np.array(a) / 255
        self.b = np.array(b) / 255
        self.c = np.array(c) / 255
        self.d = np.array(d) / 255

    def __call__(self, t:float):
        r, g, b = (self.a + self.b * np.cos(2 * pi * ((t * self.c) + self.d))) * 255
        return int(r), int(g), int(b)

def image(width, height, fname='out.png'):
    palette = CosinePalette(red, green, blue, cyan)
    x = 3 * width / 8
    y = 3 * height / 8


    # s = Stroke(1, 1, 10)
    canvas = Canvas(width, height)

    for (a, b) in linspace((x, y), (x, y + (height / 4)), 5):
        s = choice(S)
        s.w = 5
        s(linspace((a, b), (a + (width / 4), b), 20), canvas, color=palette(random()))

    canvas.save(fname=fname)


width, height, path = info()
image(width, height, path)
