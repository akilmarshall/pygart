from pygart.util import info
from pygart.color import CosinePalette, solarized
from pygart.canvas import Canvas
from PIL import ImageDraw


def dot(x, y, r, width, color, canvas):
    xy = [(x - r, y - r), (x + r, y + r)]
    ImageDraw.Draw(canvas.img).ellipse(xy, fill=color, width=width)


def dash(x, y, dash, width, color, canvas):
    xy = [(x, y), (x + dash, y)]
    ImageDraw.Draw(canvas.img).line(xy, fill=color, width=width)


def dashed_dot_line(x, y, n, dash, r, width, color, canvas, offset=0):
    gap = dash // 2
    for i in range(n):
        h = (x + offset) + (i * (gap + dash))
        u = h + dash + gap // 2
        dash(h, y, dash, width, color, canvas)
        dot(u, y, r, width, color, canvas)


def rect(x, y, side, color, canvas: Canvas, g=4):
    xy = [(x + g - 2, y + 2 * g), (x + 2 + side - g, y + g + side // 2)]
    ImageDraw.Draw(canvas.img).rounded_rectangle(xy, radius=4, fill=color)


def row(x, y, n, dash, r, width, color, pallet, canvas, offset=0):
    gap = dash // 2
    for i in range(n):
        h = (x + offset) + (i * (gap + dash))
        u = h + dash + gap // 2
        dash(h, y, dash, width, color, canvas)
        dot(u, y, r, width, color, canvas)
        rect(h, y, dash, pallet(), canvas)


class Wall():

    """Regular and askew walls"""

    def __init__(self, cols: int, rows: int, length: int, line_width: int, r: float, line_color, pallet):
        """
        :cols: number of segment circle 'columns'
        :rows: number of rows in the wall
        :length: length of each line segment
        :line_width: line width
        :r: radius of the circles
        :line_color: color of the lines and circles
        :pallet: color pallet of the rectangles

        """

        self._cols = cols
        self._rows = rows
        self._length = length
        self._line_width = line_width
        self._r = r
        self._line_color = color
        self._pallet = pallet

    def __call__(self, canvas: Canvas, x: int, y: int, askew=False):
        """
        :canvas: Canvas object to draw on
        :x: upper left corner of the wall
        :y: upper left corner of the wall
        :askew: if True produces a "brick" wall offset

        """

        for i in range(self._rows):
            delta = (self._length // 2) + self._length // 4
            k = y + (i * delta)
            offset = (i % 2) * delta * (1 if askew else 0)
            row(x, k, n, l, r, width, self._line_color, self._pallet, canvas, offset=offset)


width, height, path = info()
canvas = Canvas(width, height)
x, y = width // 5, height // 5

n = 6   # length of dotted segments
rows = 8  # number of rows
l = 50  # length of segment
width = 2  # line width
r = 1.5  # dot radius
color = solarized['base00']
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
p3 = CosinePalette(
            solarized['base2'],
            solarized['blue'],
            solarized['green'],
            solarized['base03'],
        )
pallet = CosinePalette(
            solarized['base2'],
            solarized['red'],
            solarized['green'],
            solarized['base01'],
        )

wall = Wall(6, 8, 50, 2, 1.5, color, pallet)
wall(canvas, x, y, False)
canvas.save(path)
