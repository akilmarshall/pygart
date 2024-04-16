from pygart import make_canvas
from pygart.grid import Aligned 
from pygart.two_by_two import Staple_3, pick_orientation


data = {
        'width': 500,
        'height': 500,
        'w': 80,
        'weight': 1,
        'bg': (238,	232, 213),
        'out': (220, 50, 47),
        'fill': (203, 75, 22),
    }

img, draw = make_canvas(data)

for x, y in Aligned(5, 5, data['width'], data['height'], x_off=10, y_off=10):
    Staple_3(x, y, data).draw(pick_orientation(), draw)

draw.flush()
img.save('linear_test.png')
