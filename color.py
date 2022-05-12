'''
Named colors, color palettes, and other color functions
'''
from math import pi
from random import choice, random

import numpy as np


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


def RGBA(color: tuple[int, int, int], a:float=1.) -> tuple[int, int, int, int]:
    '''
    Convert an RGB color tuple into an RGBA color with a parameter (0, 1] specifying intensity. 
    RGB values are 8 bit i.e. in [0, 255]
    '''
    return (*color, int(a * 255))


class PaletteRNG:
    '''
    A simple uniformly random color pallet over some intial set of colors
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
