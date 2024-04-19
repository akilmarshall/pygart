from itertools import cycle
from random import shuffle
from pathlib import Path

from pygart import taisho_palette, current_month, make_canvas
from pygart.two_by_two import ORIENTATIONS, \
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

XY = [(1/4, 1/4), (1/2, 1/4), (1/4, 1/2), (1/2, 1/2)]
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

    for (orientation, (x, y)) in zip(ORIENTATIONS, XY):
            obj(data['width'] * x, data['height'] * y, orientation, data, draw)

    draw.flush()
    output_path = example_dir / f'{obj.__name__.lower()}.png'
    img.save(output_path)
    print(f'wrote out: {output_path}')
