from pygart import info, Canvas, ComplexBox, PaletteRNG
from itertools import product


p = PaletteRNG([(205, 175, 140), (255, 255, 255), (202, 189, 136), (148, 153, 127), (144, 121, 113)])
canvas = Canvas(*info(), p())

# scales used: 20, 50, 100, 200
s = 20
r = -s // 2
c = p()
for x, y in product(range(40), range(40)):
    ComplexBox(s, p(), p(), p(), c, c, c)(r + x * s, r + y * s, canvas)

canvas.save()
