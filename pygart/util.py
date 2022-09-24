"""
File: util.py
Description: Utility module, universal/odd functions and classes belong here
"""

from argparse import ArgumentParser
from datetime import datetime
from math import pi
from os.path import exists
from sys import argv

from .brick import Brick
from .canvas import Canvas
from .color import getsu_set 


__all__ = ['info', 'deg', 'radian', 'lerp', 'V', 'produce', 'parameters']


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

    def __floordiv__(self, d):
        return V(self.x // d, self.y // d)

    def __truediv__(self, d):
        return V(self.x / d, self.y / d)

    def __neg__(self):
        return -1 * self

def produce(unit_size=40, scale=20):
    """
    If the first argument passed to the script is 'produce' a special set of parameters are instead accepted
    python script.py produce w h ppi extra out

    scale used in production mode
    unit_size used in normal mode

    :scale:     the relative size of the unit forms
    :unit_size: the pixel size of the unit forms
    """
    match argv:
        case [_, 'produce', w, h, ppi, extra, out]:
            """
            for print production, with parameters that make it easy
            (w, h), the print dimensions in inches
            ppi, the requested pixels per inch in the resulting image
            extra, parameters
            out, the file name for the output without an extension
            """

            w = int(w)
            h = int(h)
            ppi = int(ppi)
            i = int(extra)
            resolution = ppi * V(w, h)  # resolution / scale = unit form size
            width, height = resolution()
            unit_size = width // scale

            out_fname = f'{out}({w}x{h} {ppi}ppi)'
            j = 1
            # dont overwrite 
            while exists(f'{out_fname}.png'):
                out_fname = f'{out}({w}x{h} {ppi}ppi){j}'
                j += 1
            out = f'{out_fname}.png'
            print(f'producing -> {out}')
            time = datetime.now()
            print(f'starting: {time.hour}:{time.minute:0>2d}')
        case _:
            # normal usage
            width, height, i = info()
            i = int(i)
            unit_size = 40
            out = 'out.png'
    return width, height, out, i, unit_size

def parameters(WIDTH=700, HEIGHT=700, OUT_NAME='out.png', p=0):
    """
    Defines the default parameter bundle, the parameters modify the default values defined at the CLI.
    month parameter default is unmodifyable and defaults to the month on the calender at run time.
    Built on ArgumentParser thus implements --help at the CLI.

    :WIDTH:     output width in pixels 
    :HEIGHT:    output height in pixels 
    :OUT_NAME:  output file name
    :p:         pallete index for a given month
    """
    now = datetime.now()
    MONTH = ["january" ,"february" ,"march" ,"april" ,"may" ,"june" ,"july" ,"august" ,"september" ,"october" ,"november" ,"december"][now.month - 1]

    parser = ArgumentParser()
    parser.add_argument('-width', type=int, default=WIDTH, help=f'Image width of the output in pixels. default {WIDTH}') 
    parser.add_argument('-height', type=int, default=HEIGHT, help=f'Image height of the output in pixels. default {HEIGHT}') 
    parser.add_argument('-out', type=str, default='out.png', help=f'File name of the output image. default: {OUT_NAME}') 
    parser.add_argument('-month', type=str, default=MONTH, help=f"Which month's color palletes to select from. default: {MONTH}") 
    parser.add_argument('-p', type=int, default=p, choices=[0, 1, 2, 3, 4, 5], help=f"Index of the pallete to use. default: {p}") 

    return parser.parse_args()
