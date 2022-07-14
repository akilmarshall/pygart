from pygart.util import info
from pygart.color import CosinePalette, solarized
from pygart.canvas import Canvas
from random import randint
from PIL import ImageDraw

width, height, path = info()
canvas = Canvas(width, height)
b_width, b_height = width // 20, height // 20


class Brick:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def _pos(self, x: int, y: int):
        return (x, y, x + self.width, y + self.height)

    def __call__(self, canvas, x: int, y: int, color=None):
        if color: 
            ImageDraw.Draw(canvas.img).rectangle(self._pos(x, y), fill=color)
        else:
            gap = 5
            ImageDraw.Draw(canvas.img).line(
                    [(x, y + b_height), (x + b_width, y + b_height)],
                    fill='grey',
                    width=2
                    )
            ImageDraw.Draw(canvas.img).line(
                    [(x + b_width, y), (x + b_width, y + b_height - gap)],
                    fill='grey',
                    width=2
                    )


def row_points(x, y, delta, limit):
    while x < limit:
        yield x, y
        x += delta


def brick_row(canvas, x, y, n):
    b = Brick(b_width, b_height)
    for x, y in row_points(x, y, b_width, (4 * width) // 5):
        b(canvas, x, y,)


def brick_wall(canvas, x, y, cols, rows):
    for row in range(rows):
        brick_row(canvas, x, row * b_height + y, cols)


def walk(n):
    return [randint(0, 2) for _ in range(n)]


def apply(d, x, y):
    assert(d in [0, 1, 2])
    match d:
        case 0:
            return x + b_width, y + b_height
        case 1:
            return x + b_width, y
        case 2:
            return x + b_width, y - b_height
    return x, y


pallet = CosinePalette(
        solarized['base2'],
        solarized['red'],
        solarized['green'],
        solarized['base01'],
        )


def color_walk(canvas, x, y, n):
    b = Brick(b_width, b_height)
    for d in walk(n):
        b(canvas, x, y, pallet())
        x, y = apply(d, x, y)


def Y(y, n):
    return y + n * b_height


h, k = width // 5, height // 5
for i in range(1, 12, 2):
    color_walk(canvas, h, Y(k, i), 12)
brick_wall(canvas, h, k, 11, 13)

canvas.save(path)
