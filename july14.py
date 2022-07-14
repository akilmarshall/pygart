from pygart.util import info
from pygart.canvas import Canvas
from pygart.color import solarized, CosinePalette, PaletteRNG

from PIL import ImageDraw


GRAY = solarized['base00']
GRAY = None


def poly(polygon, color, out, weight, canvas):
    ImageDraw.Draw(canvas.img).polygon(
            polygon,
            fill=color,
            outline=out,
            width=weight
            )


def diamond(x, y, side):
    half = side // 2
    return [(x, y), (x + half, y - half), (x, y - side), (x - half, y - half)]


def half_diamond_right(x, y, side):
    half = side // 2
    return [(x, y), (x, y - half), (x + half, y - side), (x + half, y - half)]


def half_diamond_left(x, y, side):
    half = side // 2
    return [(x, y), (x, y - half), (x - half, y - side), (x - half, y - half)]


class Box:
    """Iso box"""

    def __init__(self, side, A, B, C):
        """

        :side: TODO
        :A: TODO
        :B: TODO
        :C: TODO

        """

        self._side = side
        self._A = A
        self._B = B
        self._C = C

    def __call__(self, x: int, y: int, canvas: Canvas, out=GRAY):
        poly(half_diamond_left(x, y, side), self._B, out, 2, canvas)
        poly(half_diamond_right(x, y, side), self._C, out, 2, canvas)
        poly(diamond(x, y - side // 2, side), self._A, out, 2, canvas)


class Left:

    def __init__(self, side, B):
        """

        :side: TODO
        :B: TODO

        """

        self._side = side
        self._B = B

    def __call__(self, x: int, y: int, canvas: Canvas, out=GRAY):
        poly(half_diamond_left(x, y, side), self._B, out, 2, canvas)


class Right:

    def __init__(self, side, C):
        """

        :side: TODO
        :C: TODO

        """

        self._side = side
        self._C = C

    def __call__(self, x: int, y: int, canvas: Canvas, out=GRAY):
        poly(half_diamond_right(x, y, side), self._C, out, 2, canvas)


def row(x, y, side, n, A, B, C, canvas):
    Box(side, A(), B(), C())(x, y, canvas)
    half = side // 2
    for i in range(0, n):
        Box(side, A(), B(), C())(x + i * side, y, canvas)
        Box(side, A(), B(), C())(x + half + i * side, y + side, canvas)


def wall(x, y, cols, rows, A, B, C, canvas):
    for i in range(rows):
        row(x, y + i * 2 * side, side, cols, A, B, C, canvas)


pallet = CosinePalette(
        solarized['base2'],
        solarized['red'],
        solarized['green'],
        solarized['base01'],
        )
brick_pallet = PaletteRNG([(150, 41, 56), (170, 47, 64), (190, 52, 71), (203, 65, 84), (208, 85, 102), (214, 105, 120), (219, 125, 138)]) 
offwhite = PaletteRNG([(217, 217, 217), (230, 230, 230), (242, 242, 242)])

width, height, path = info()
x, y = width // 2, height // 2
canvas = Canvas(width, height)
side = 50

wall(0, side, 11, 7, pallet, pallet, pallet, canvas)
canvas.save(path)
