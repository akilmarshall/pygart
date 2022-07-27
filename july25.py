from math import sin, pi
from pygart import Canvas, ComplexBox, getsu_set, PaletteRNG, RGBA
from PIL import ImageDraw


class Lissajous:
    '''
    Lissajous curve in the plane
    '''

    def __init__(self, A, B, a, b, delta):
        self.A = A
        self.B = B
        self.a = a
        self.b = b
        self.delta = delta

    def x(self, t):
        '''A * sin(a * t + delta) '''
        return self.A * sin(self.a * t + self.delta)

    def y(self, t):
        '''B * sin(b * t) '''
        return self.B * sin(self.b * t)

    def __call__(self, t):
        return (self.x(t), self.y(t))


def lerp(a, b, t):
    return a + b * t

width, height = 500, 500
r = 1
n = 750  # number of sub units in the figure
s = 10
# r = -s // 2
p = PaletteRNG(list(getsu_set('july'))[3])
canvas = Canvas(width, height)

xoff, yoff = 250, 250
colors = {}
frames = 1000  # number of frames to divide the full rotation into
for offset in range(frames):
    canvas = Canvas(width, height)
    draw = ImageDraw.Draw(canvas.img)
    t = offset / frames
    lissa = Lissajous(200, 200, lerp(7, 9, t), lerp(9, 13, t), lerp(0, 4 * pi, t))  # step through all orientations
    for i in range(n):
         # lissajous is periodic in [0, 2pi)
        theta = 2 * pi * i / n
        a, b = lissa(theta)
        c, d = lissa(theta + pi / 2)
        if i in colors:
            color = colors[i]
        else:
            color = p()
            colors[i] = color
        draw.line((a + xoff, b + yoff, c + xoff, d + yoff), fill=RGBA(color, 0.5), width=2)
    canvas.save(f'frames/{offset}.png')
