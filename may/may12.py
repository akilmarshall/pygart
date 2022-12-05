from pygart.canvas import Canvas
from pygart.util import info
from pygart.color import solarized, CosinePalette
from pygart.lsystem import apply, BOL, TreeA, TreeB, TreeC, Turtle
from random import choice, random
from itertools import product

from math import pi


width, height, path = info()
canvas = Canvas(width, height, solarized['base3'])
deg = lambda theta: (pi/180)*theta
trees = [(apply(3, TreeC), 6, deg(22.5)), (apply(4, TreeB), 6, deg(20)), (apply(4, TreeA), 2, deg(25.))]
palette = CosinePalette((95, 113, 97), (109, 139, 116), (239, 234, 216), (208, 201, 192))
# part 1
'''
for x, y in ellipse((width//2), 5*(height//8), 150, 150, 10, pi/5):
    tree, d, a = choice(trees)
    sign = choice([-1, 1])
    BOL(canvas, tree, d,a, Turtle(x, y, deg(270), sign), color=palette()) 
'''

mod = [-1, 0, 0, 1]

row = 3
col = 3
dx = width//col
dy = height//row
for x, y in product(range(1, row + 1), range(1, col + 1)):
    tree, d, a = choice(trees)
    sign = choice([-1, 1])
    m = choice(mod)
    px = (x * dx) - (dx/2)
    py = (y * dy) - (dy/2)
    BOL(canvas, tree, d + m, a + random(), Turtle(px, py, deg(270), sign), color=palette()) 


canvas.save(path)
