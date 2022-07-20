from pygart.util import info
from pygart.canvas import Canvas
from pygart.brick import Brick
from pygart.color import getsu_set, RGBA, solarized

from PIL import ImageDraw
from itertools import product
from random import random, choice


GRAY = RGBA(solarized['base00'], 0.75)


def window(x, y, w, h, trim, a, b, c, canvas):
    Brick(w, h)(canvas, x, y, a)
    D = w - 3 * trim
    left = D // 3
    right = (2 * D) // 3
    sub_height = h - 2 * trim
    Brick(left, sub_height)(canvas, x + trim, y + trim, b)
    Brick(right, sub_height)(canvas, x + trim * 2 + left, y + trim, c)


class Room:
    def __init__(self, width, height, offset, palette, window_chance=0.5, room_chance=0.9):
        self.width = width
        self.height = height
        self.palette = palette
        self.window_chance = window_chance
        self.room_chance = room_chance

        self.offset = offset

    def roll_window(self):
        return random() < self.window_chance

    def roll_room(self):
        return random() < self.room_chance

    def room(self, canvas, x, y, fill):
        Brick(self.width, self.height)(canvas, x, y, color=fill)

    def x(self, canvas, x, y, n, gap, color):
        width = self.width // n
        height = self.height
        mx, my = x + width // 2, y + height // 2
        a = x + width
        b = y + height

        xy = [x, y, mx, my - gap, a, y, mx + gap, my, a, b, mx, my + gap, x, b, mx - gap, my]
        ImageDraw.Draw(canvas.img).polygon(xy, fill=color, width=1)

    def window(self, canvas, x, y, a, b, c):
        dx, dy = self.offset
        width = (self.width // 2) - 2 * dx
        height = self.height - 2 * dx
        window(
                x + dx,
                y + dy,
                width,
                height - dy,
                4,
                a, b, c, canvas)

    def color(self):
        return choice(self.palette)

    def __call__(self, x, y, canvas):
        self.room(canvas, x, y, choice(self.palette))
        if self.roll_room():
            self.window(canvas, x, y, self.color(), self.color(), self.color())
            self.window(canvas, x + self.width // 2, y, self.color(), self.color(), self.color())
        else:
            n = 5
            c = self.color()
            for i in range(n):
                self.x(canvas, x + i * self.width // n, y, n, 3, c)


def building(x, y, width, height, rows, columns, palette, canvas):
    for r, c in product(range(rows), range(columns)):
        h = x + r * width
        k = y + c * height
        Room(width, height, (15, 15), palette)(h, k, canvas)


P = list(getsu_set('july'))

width, height, path = info()
canvas = Canvas(width, height)

for i, p in enumerate(P):
    building(0, 0, 150, 75, 3, 6, P[i], canvas)
    canvas.save(f'{path}{i}.png')
