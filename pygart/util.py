"""
File: util.py
Description: Utility module, universal/odd functions and classes belong here
"""

from sys import argv
from math import pi
from .brick import Brick
from .color import getsu_set
from .canvas import Canvas


__all__ = ['info', 'deg', 'radian',]


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

