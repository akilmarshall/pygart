from scipy.stats import beta
from functools import partial
from color import *
from canvas import *
from PIL import ImageDraw
from itertools import combinations


class Characteristic:
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        fx = self.f(x)
        return max(0, fx)


# change the argument order for use with partial
def _beta_helper(a, b, x): return beta.pdf(x, a, b)
def alphabeta(a, b): return partial(_beta_helper, a, b)


class Stroke:
    def __init__(self, a, b, w=3):
        """
        (a, b) line parameters, w stroke weight
        """
        self.c = alphabeta(a, b)
        self.w = w

    def __call__(self, path, canvas, color=RGBA(base03)):
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

# list of ready to use characteristics

S = [Stroke(a, b) for (a, b) in combinations(range(1, 6), 2)]
