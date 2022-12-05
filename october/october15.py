from itertools import product
from math import cos, pi, sin

from aggdraw import Draw, Pen, Brush

from pygart import Canvas, PaletteRNG, V, parameters, month_palette, line, PaletteOrdered, ground_colors, sky_colors
from random import shuffle, choice, random


args = parameters(WIDTH=500, HEIGHT=500)
# bg, p = ground_colors(list(month_palette(args.month, args.p)))
bg, p = sky_colors(list(month_palette(args.month, args.p)))
canvas = Canvas(args.width, args.height, color=bg)
draw = Draw(canvas.img)

n = 60
m = 20

# pal = PaletteOrdered(p)
pal = PaletteRNG(p)

delta_n = args.width / (n )
delta_m = args.height / (m )

cols = [delta_n * V(i, 0) for i in range(n )]
rows = [delta_m * V(0, i) for i in range(m )]

points = cols + rows
shuffle(points)

action_col = V(args.width / (n ), 0)
action_row = V(0, args.height / (m ))
action_width = V(args.width, 0)
action_height = V(0, args.height)

def pen(c, w):
    return Pen(c, w)

def brush(c):
    return Brush(c)


w = 4
for p in points:
    if p.x == 0:
        # row
        points = [p]
        points.append(points[-1] + action_width)
        points.append(points[-1] + action_row)
        points.append(points[-1] - action_width)
        points.append(points[-1] - action_row)
        draw.polygon(sum([point() for point in points], ()), brush(pal()), pen(bg, w))
    else:
        # col
        if random() < 0.4:
            continue
        points = [p]
        points.append(points[-1] + action_height)
        points.append(points[-1] + action_col)
        points.append(points[-1] - action_height)
        points.append(points[-1] - action_col)
        draw.polygon(sum([point() for point in points], ()), brush(pal()), pen(bg, w))

draw.flush()
canvas.save(args.out)
