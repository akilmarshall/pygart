"""
File: stroke.py
Description: Drawing parametric strokes
"""

from functools import partial

from PIL import ImageDraw
from scipy.stats import beta

from .color import RGBA, solarized


__all__ = ['Stroke']

# change the argument order for use with partial
def _beta_helper(a, b, x): return beta.pdf(x, a, b)
def alphabeta(a, b): return partial(_beta_helper, a, b)


class Stroke:
    """A parameteric stroke type. """

    def __init__(self, a, b, w=3):
        """
        (a, b) line parameters, w stroke weight
        """
        self.c = alphabeta(a, b)
        self.w = w

    def __call__(self, path, canvas, color=RGBA(solarized['base03'])):
        '''
        path: [(int, int)]
        r: float
        canvas: Image
        '''
        draw = ImageDraw.Draw(canvas.img)
        n = len(path)
        for i, (x, y) in enumerate(path):
            r = self.w * self.c(i / n)
            a, b = x - self.w, y - r
            c, d = x + self.w, y + r
            draw.ellipse((a, b, c, d), fill=color)

