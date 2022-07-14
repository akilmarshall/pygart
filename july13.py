from pygart.util import info
from pygart.color import CosinePalette, solarized
from pygart.canvas import Canvas
from PIL import ImageDraw


def dot(x, y, r, width, color, canvas):
    xy = [(x - r, y - r), (x + r, y + r)]
    ImageDraw.Draw(canvas.img).ellipse(xy, fill=color, width=width)


def dash_h(x, y, dash, width, color, canvas):
    xy = [(x, y), (x + dash, y)]
    ImageDraw.Draw(canvas.img).line(xy, fill=color, width=width)


def dash_v(x, y, dash, width, color, canvas):
    xy = [(x, y), (x, y + dash)]
    ImageDraw.Draw(canvas.img).line(xy, fill=color, width=width)


def dashed_dot_line_h(x, y, n, dash, r, width, color, canvas, offset=0):
    gap = dash // 2
    for i in range(n):
        h = (x + offset) + (i * (gap + dash))
        u = h + dash + gap // 2
        dash_h(h, y, dash, width, color, canvas)
        dot(u, y, r, width, color, canvas)


def rect(x, y, side, color, canvas: Canvas, g=4):
    xy = [(x + g - 2, y + 2 * g), (x + 2 + side - g, y + g + side // 2)]
    ImageDraw.Draw(canvas.img).rounded_rectangle(xy, radius=4, fill=color)


def row(x, y, n, dash, r, width, color, pallet, canvas, offset=0):
    gap = dash // 2
    for i in range(n):
        h = (x + offset) + (i * (gap + dash))
        u = h + dash + gap // 2
        dash_h(h, y, dash, width, color, canvas)
        dot(u, y, r, width, color, canvas)
        rect(h, y, dash, pallet(), canvas)


width, height, path = info()
canvas = Canvas(width, height)
x, y = width // 5, height // 5

n = 6   # length of dotted segments
rows = 8  # number of rows
l = 50  # length of segment
width = 2  # line width
r = 1.5  # dot radius
p1 = CosinePalette(
            solarized['base1'],
            solarized['magenta'],
            solarized['blue'],
            solarized['base03'],
        )
p2 = CosinePalette(
            solarized['base01'],
            solarized['red'],
            solarized['green'],
            solarized['base03'],
        )
pallet = CosinePalette(
            solarized['base2'],
            solarized['blue'],
            solarized['green'],
            solarized['base03'],
        )
color = solarized['base00']

row(x, y, 5, l, r, width, color, pallet, canvas)
for i in range(rows):
    delta = (l // 2) + l // 4
    k = y + (i * delta)
    offset = (i % 2) * delta
    row(x, k, n, l, r, width, color, pallet, canvas, offset=offset)

canvas.save(path)
