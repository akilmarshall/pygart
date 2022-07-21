"""
File: color.py
Description: Named colors, color palettes, and other color functions
"""

from math import pi
from random import choice, random
from itertools import permutations
import json

import numpy as np


__all__ = [
        'solarized',
        'getsu',
        'getsu_set',
        'RGBA',
        'PaletteRNG',
        'CosinePalette',
        'to_hsv',
        'to_rgb',
        ]


# named solarized colors
solarized = {
    'base03':  (0, 43, 54),
    'base02':  (7, 54, 66),
    'base01':  (88, 110, 117),
    'base00':  (101, 123, 131),
    'base0':  (131, 148, 150),
    'base1':  (147, 161, 161),
    'base2':  (238, 232, 227),
    'base3':  (253,  246, 227),
    'yellow':  (181, 137, 0),
    'orange':  (203, 75, 22),
    'red':  (220, 50, 47),
    'magenta':  (211, 54, 130),
    'violet':  (108, 113, 196),
    'blue':  (38, 139, 210),
    'cyan':  (42, 161, 152),
    'green':  (133, 153, 0),
}


def taisho_color(color):
    if color in color_dict:
        r, g, b = color_dict[color]
        return r, g, b


# taisho-showa-color-vocab.json
color_dict = None
palette_dict = None
with open('pygart/taisho-showa-color-vocab.json') as f:
    color_dict = json.load(f)
with open('pygart/taisho-showa-palettes.json') as f:
    palette_dict = json.load(f)


def getsu(i):
    def T(a):
        return list(map(taisho_color, a))
    p = palette_dict['pallete'][i]
    return T(p)


def getsu_set(month):
    if month in palette_dict:
        for i in palette_dict[month]:
            yield getsu(i)


def RGBA(color: tuple[int, int, int], a: float = 1.) -> tuple[int, int, int, int]:
    '''
    Convert an RGB color tuple into an RGBA color with a parameter (0, 1]
    specifying intensity. RGB values are 8 bit i.e. in [0, 255]
    '''
    return (*color, int(a * 255))


class PaletteRNG:
    '''
    A simple uniformly random color pallete over some intial set of colors
    '''

    def __init__(self, colors):
        self.colors = colors

    def __call__(self):
        return choice(self.colors)


class CosinePalette:
    def __init__(self, a, b, c, d):
        self.a = np.array(a) / 255  # type: ignore
        self.b = np.array(b) / 255  # type: ignore
        self.c = np.array(c) / 255  # type: ignore
        self.d = np.array(d) / 255  # type: ignore

    def __call__(self, t=None):
        if t is None:
            t = random()
        r, g, b = (self.a + self.b * np.cos(2 * pi * ((t * self.c) + self.d))) * 255
        return int(r), int(g), int(b)


class CosinePaletteRNG:
    '''
    Given colors create a random cosine color palettes
    Palette() emits colors
    '''

    def __init__(self, colors: list):
        '''
        colors  a list of rgb colors, 4 or more.
        '''
        assert len(colors) > 3
        self.colors = colors

        self._setup_palette()

    def _setup_palette(self):
        self.a, self.b, self.c, self.d = choice(
                list(permutations(self.colors, r=4)))
        self.palette = CosinePalette(self.a, self.b, self.c, self.d)

    def __call__(self, t=None):
        return self.palette(t)


def to_hsv(r: int, g: int, b: int) -> tuple[int, float, float]:
    """
    Convert 8bit rgb channels into (hue, saturation, value)
    """
    assert(0 <= r < 256)
    assert(0 <= g < 256)
    assert(0 <= b < 256)

    def max_channel():
        if r > g and r > b:
            return 'r'
        elif g > r and g > b:
            return 'g'
        elif b > r and b > g:
            return 'b'
    r = r/255
    g = g/255
    b = b/255
    Cmax = max(r, g, b)
    delta = Cmax - min(r, g, b)

    def hue():
        match max_channel():
            case 'r':
                return 60 * (((g - b) / delta) % 6)
            case 'g':
                return 60 * (((b - r) / delta) + 2)
            case 'b':
                return 60 * (((r - g) / delta) + 4)

        return 0

    def saturation():
        if Cmax == 0:
            return 0
        return delta / Cmax

    return hue(), saturation(), Cmax


def to_rgb(h: int, s: float, v: float) -> tuple[int, int, int]:
    """
    Convert a (hue, saturation, value) color into (r, g, b)
    """
    assert(0 <= h < 360)
    assert(0 <= s <= 1)
    assert(0 <= v <= 1)
    c = v * s
    x = c * (1 - abs(((h / 60) % 2) - 1))
    m = v - c

    def RGB():
        if 0 <= h < 60:
            return c, x, 0
        elif 60 <= h < 120:
            return x, c, 0
        elif 120 <= h < 180:
            return 0, c, x
        elif 180 <= h < 240:
            return 0, x, c
        elif 240 <= h < 300:
            return x, 0, c
        elif 300 <= h < 360:
            return c, 0, x

    r, g, b = RGB()
    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
