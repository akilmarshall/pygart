# from pygart import info, Canvas, draw, PaletteRNG, getsu_set
from pygart import info, Canvas, getsu_set, PaletteRNG
from itertools import product

from PIL import ImageDraw
from random import choice


def box(x, y, r, delta, color, w, weights, canvas):
    draw = ImageDraw.Draw(canvas.img)
    third = r // 3
    A = [(x, y), (x + r - delta, y)]
    B = [(x + r, y), (x + r, y + r - delta)]
    C = [(x + r, y + r), (x + delta, y + s)]
    D = [(x, y + r), (x, y + delta)]
    E = [(x + third, y + third), (x + 2 * third, y + third), (x + 2 * third, y + 2 * third), (x + third, y + 2 * third)]
    if choice(weights):
        draw.line(A, width=w, fill=color)
    if choice(weights):
        draw.line(B, width=w, fill=color)
    if choice(weights):
        draw.line(C, width=w, fill=color)
    if choice(weights):
        draw.line(D, width=w, fill=color)
    if choice(weights):
        draw.polygon(E, width=w, fill=color)


colors = list(getsu_set('august'))[5]
p = PaletteRNG(colors)

for num, bg in enumerate(colors):
    canvas = Canvas(*info(), color=bg)
    s = 25 
    cols = 20 
    rows = 20 

    for i, j in product(range(cols), range(rows)):
        x = i * s
        y = j * s
        box(x, y, s, 3, p(), 2,[True, False, True, True, False], canvas) 

    canvas.save(f'{num}.png')
