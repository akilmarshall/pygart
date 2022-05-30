from math import sqrt, cos, sin, pi
from PIL import ImageDraw
from color import RGBA, solarized


class Region:
    def __init__(self, x, y, width, height, theta=0.):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.theta = theta

    def points(self):
        a = self.width / 2
        b = self.height / 2
        c = sqrt(a**2 + b**2)
        left = pi * a / b
        right = pi * (1 - (a / b))
        # out = [ left * pi, right * pi, left * 2 * pi, right * 2 * pi]
        # out = [
        #         (self.x + a, self.y + b),
        #         (self.x - a, self.y + b),
        #         (self.x - a, self.y - b),
        #         (self.x + a, self.y - b),
        #         ]
        # def t(t):
        #     x, y = t
        #     x -= self.x
        #     y -= self.y
        #     x = x * cos(self.theta) - y * sin(self.theta)
        #     y = x * sin(self.theta) + y * cos(self.theta)
        #     return x + self.x, y + self.y


        # return list(map(t, out))

    def __call__(self, canvas, color=RGBA(solarized['base03'])):
        '''
        path: [(int, int)]
        r: float
        canvas: Image
        '''
        ImageDraw.Draw(canvas.img).polygon(self.points(), outline=color)

    # def contain(self, x, y) -> bool:
    #     if 
