from itertools import cycle
from random import shuffle
from pathlib import Path

from pygart import taisho_palette, current_month, make_canvas
from pygart.two_by_two import Orientation, \
    Rectangular_Prism, Triangular_Prism, \
    Half_Triangular_Prism, Half_Triangular_Prism_Mirror, \
    Triangular_Prism_2, Tent, \
    Staple, Staple_2


palettes = list(taisho_palette(current_month()))
shuffle(palettes)
objs = [
        Rectangular_Prism,
        Triangular_Prism,
        Half_Triangular_Prism,
        Half_Triangular_Prism_Mirror,
        Triangular_Prism_2,
        Tent,
        Staple,
        Staple_2,
        ]
example_dir = Path('example')

if not example_dir.exists():
    example_dir.mkdir()


for palette, obj in zip(cycle(palettes), objs):
    shuffle(palette)
    data = {
            'width': 500,
            'height': 500,
            'w': 100,
            'weight': 1,
            'bg': palette[0],
            'out': palette[1],
            'fill': palette[2]
        }
    img, draw = make_canvas(data)

    obj(Orientation.NORTH, data['width'] / 4, data['height'] / 4, data['w']) \
        .draw(draw, data)
    obj(Orientation.SOUTH, data['width'] / 2, data['height'] / 4, data['w']) \
        .draw(draw, data)
    obj(Orientation.EAST, data['width'] / 4, data['height'] / 2, data['w']) \
        .draw(draw, data)
    obj(Orientation.WEST, data['width'] / 2, data['height'] / 2, data['w']) \
        .draw(draw, data)

    draw.flush()
    img.save(example_dir / f'{obj.__name__.lower()}.png')
