from random import random, shuffle

# from PIL import ImageDraw
from aggdraw import Draw, Pen, Brush

from pygart import Canvas, parameters, month_palette


args = parameters()
# width, height, path = info()
s = 30
# colors = list(getsu_set('august'))[5]
colors = list(month_palette(args.month, args.p))
width = args.width
height = args.height

p3 = colors[0]
for c in colors:
    if sum(c) <= sum(p3):
        p3 = c

shuffle(colors)
bg = colors.pop()
p1 = colors.pop()
p2 = colors.pop()

canvas = Canvas(width, height, color=bg)
draw = Draw(canvas.img)

w = 1


def vertical(x, y, a, b):
    pen = Pen(b, w)
    brush = Brush(a)
    X = x + s
    Y = y + 3 * s
    draw.polygon((x, y, X, y, X, Y, x, Y), pen, brush)


def horizontal(x, y, a, b):
    pen = Pen(b, w)
    brush = Brush(a)
    X = x + 3 * s
    Y = y + s
    draw.polygon((x, y, X, y, X, Y, x, Y), pen, brush)


def row(y, a, b):
    pen = Pen(b, w)
    brush = Brush(a)
    Y = y + s
    draw.polygon((0, y, width, y, width, Y, 0, Y), pen, brush)


def col(x, a, b):
    pen = Pen(b, w)
    brush = Brush(a)
    X = x + s
    draw.polygon((x, 0, X, 0, X, height, x, height), pen, brush)


W = width // s
H = height // s
X = list(range(W))
Y = list(range(H))
shuffle(X)
shuffle(Y)
T = 0.75


# RNG weave
for x, y in zip(X, Y):
# ordered weave
# for x, y in zip(range(W), range(H)):
    x *= s
    y *= s
    if random() < T:
        row(y, p1, p3)
    if random() < T:
        col(x, p2, p3)
draw.flush()
canvas.save(args.out)
