"""
Provides isometric drawing and other iso utilities
"""
from .canvas import Canvas
from PIL import ImageDraw


__all__  = [
        'ComplexBox',
        'Left',
        'Right',
        ]


def draw(polygon, color, out, weight, canvas):
    """
    draw a polygon
    """
    ImageDraw.Draw(canvas.img).polygon(
            polygon,
            fill=color,
            outline=out,
            width=weight
            )


def diamond(x, y, side, n=1, m=1):
    """
    Return the xy positions of points describing a diamond at (x, y).
      a
    d   b
      c
    """
    half = side // 2
    a = (x + n * half, y - m * half)
    b = (x, y - m * side)
    c = (x - n * half, y - m * half)
    return [(x, y), a, b, c]


def parallelogram_right(x, y, side, n=1, m=1):
    """
    Return the xy position of a right handed parallelogram
    """
    half = side // 2
    a = (x, y - m * half)
    b = (x + n * half, y - m * half)
    c = (x + n * half, y - m * half)
    return [(x, y), a, b, c]


def parallelogram_left(x, y, side, n=1, m=1):
    """
    Return the xy position of a left handed parallelogram
    """
    half = side // 2
    a = (x, y - m * half)
    b = (x - n * half, y - m * side)
    c = (x - n * half, y - m * half)
    return [(x, y), a, b, c]


class ComplexBox:
    """
    Class for drawing a Complex Iso box
    """

    def __init__(self, side, A, B, C, a, b, c):
        self.side = side
        self.A = A
        self.B = B
        self.C = C
        self.a = a
        self.b = b
        self.c = c

        self.half = self.side // 2

    def u(self, x, y, m):
        return x + m * self.half, y + m * self.half

    def i(self, x, y, n, m):
        return x + (m - n) * self.half, y + (n + m) * self.half

    def o(self, x, y, n):
        return x - n * self.half, y + n * self.half

    def diamond(self, x: int, y: int, n: int, m: int):
        """
         (x, y)
        o      u
           i
        """
        return [(x, y), self.u(x, y, m), self.i(x, y, n, m), self.o(x, y, n)]

    def apply(self, P, h):
        return P[0], P[1] + h * self.half

    def left(self, x, y, n, m, h):
        u = self.o(x, y, n)
        v = self.i(x, y, n, m)
        return [u, v, self.apply(v, h), self.apply(u, h)]

    def right(self, x, y, n, m, h):
        w = self.u(x, y, m)
        v = self.i(x, y, n, m)
        return [w, v, self.apply(v, h), self.apply(w, h)]

    def __call__(self, x: int, y: int, canvas: Canvas, n=1, m=1, h=1):
        draw(self.diamond(x, y, n, m), self.A, self.a, 2, canvas)
        draw(self.left(x, y, n, m, h), self.B, self.b, 2, canvas)
        draw(self.right(x, y, n, m, h), self.C, self.c, 2, canvas)


class Left:
    """
    Class for drawing left handed parallelogram
    """

    def __init__(self, side, B, out):
        """

        :side: TODO
        :B: TODO

        """

        self.side = side
        self.B = B
        self.out = out

    def __call__(self, x: int, y: int, canvas: Canvas):
        draw(parallelogram_left(x, y, self.side), self.B, self.out, 2, canvas)


class Right:
    """
    Class for drawing right handed parallelogram
    """

    def __init__(self, side, C, out):
        """

        :side: TODO
        :C: TODO

        """

        self.side = side
        self.C = C
        self.out = out

    def __call__(self, x: int, y: int, canvas: Canvas):
        draw(parallelogram_right(x, y, self.side), self.C, self.out, 2, canvas)
