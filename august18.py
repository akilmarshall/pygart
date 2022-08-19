from random import random, shuffle

from PIL import ImageDraw

from pygart import Canvas, getsu_set, info


width, height, path = info()
s = 25
colors = list(getsu_set('august'))[5]

p3 = colors[0]
for c in colors:
    if sum(c) <= sum(p3):
        p3 = c

shuffle(colors)
bg = colors.pop()
p1 = colors.pop()
p2 = colors.pop()

canvas = Canvas(width, height, color=bg)
draw = ImageDraw.Draw(canvas.img)

w = 1
def vertical(x, y, a, b):
    draw.rectangle((x, y, x + s, y + 3 * s), fill=a, outline=b, width=w) 

def horizontal(x, y, a, b):
    draw.rectangle((x, y, x + 3 * s, y + s), fill=a, outline=b, width=w) 

def row(y, a, b):
    draw.rectangle((0, y, width, y + s), fill=a, outline=b, width=w)

def col(x, a, b):
    draw.rectangle((x, 0, x + s, height), fill=a, outline=b, width=w)

W = width // s
H = height // s
X = list(range(W))
Y = list(range(H))
shuffle(X)
shuffle(Y)

# RNG weave
for x, y in zip(X, Y):
# ordered weave
# for x, y in zip(range(W), range(H)):
    if random() < 0.75:
        row(y * s, p1, p3)
    if random() < 0.75:
        col(x * s, p2, p3)
canvas.save()
