from canvas import Canvas
from util import info
from lsystem import *
from color import solarized, Palette, CosinePalette
from path import ellipse
from random import choice, random

from math import pi


width, height, path = info()
canvas = Canvas(width, height, solarized['base3'])
deg = lambda theta: (pi/180)*theta
trees = [(apply(3, TreeC), 6, deg(22.5)) , (apply(4, TreeB), 6, deg(20)), (apply(4, TreeA), 2, deg(25.))]
palette = CosinePalette((95, 113, 97), (109, 139, 116), (239, 234, 216), (208, 201, 192))


for x, y in ellipse((width//2), 5*(height//8), 150, 150, 10, pi/5):
    tree, d, a = choice(trees)
    sign = choice([-1, 1])
    BOL(canvas, tree, d,a, Turtle(x, y, deg(270), sign), color=palette()) 

canvas.save(path)
