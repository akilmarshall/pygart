from canvas import Canvas
from util import info
# from lsystem import DOL, Turtle, apply,
from lsystem import *

from math import pi


width, height, path = info()
canvas = Canvas(width, height)

DOL(canvas, apply(2, GosperQuad), 5, pi/2, Turtle(width/2, height/2, 0))

canvas.save(path)
