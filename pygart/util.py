"""
File: util.py
Description: Utility module, universal/odd functions and classes belong here
"""

from sys import argv
from math import pi
from .brick import Brick
from .color import getsu_set
from .canvas import Canvas


__all__ = ['info', 'deg', 'radian', 'lerp', 'V']


def info():
    match argv:
        case [_, width, height, path]:
            return int(width), int(height), path
        case _:
            print("usage: width heigh <path>.png")
            print(f"got {argv}")
            quit()


def deg(radian: float) -> float:
    return pi / 180 * radian


def radian(deg: float) -> float:
    return pi * 180 * deg


def getsu_palette_sample(
        x: int,
        y: int,
        side: int,
        gap: int,
        month: str,
        canvas: Canvas):
    def color_row(x, y, side, colors, canvas):
        b = Brick(side, side)
        for i, c in enumerate(colors):
            b(canvas, x + i * side, y, c)

    for i, p in enumerate(list(getsu_set(month))):
        h, k = x + gap, y + i * (side + gap)
        color_row(h, k, side, p, canvas)


def lerp(A: int, B: int, t: float) -> float:
    '''Linear interpolation between A and B by t'''
    return min(A, B) + t * max(A, B)

class V:
    """
    A simple class representing a 2D vector over Z
    adds in the usual way
    """
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def v(self) -> tuple[float, float]:
        return int(self.x), int(self.y)

    def __add__(self, other):
        return V(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + V(-other.x, -other.y)

    def __call__(self):
        return self.v()

    def __repr__(self):
        return f'V({self.x}, {self.y})'
    
    def __mul__(self, s):
        return V(self.x * s, self.y * s)

    def __rmul__(self, s):
        return V(self.x * s, self.y * s)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
