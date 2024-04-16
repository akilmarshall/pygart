from argparse import ArgumentParser
from itertools import permutations
from random import choice, shuffle, randint
from pathlib import Path

from pygart import current_month, taisho_palette, make_canvas
from pygart.grid import Aligned
from pygart.two_by_two import Orientation, \
    Rectangular_Prism, Triangular_Prism, \
    Half_Triangular_Prism, Half_Triangular_Prism_Mirror, \
    Triangular_Prism_2, Tent, \
    Staple, Staple_2

from tqdm import tqdm

DEFAULT_WEIGHT = 1
DEFAULT_MONTH = current_month()
DEFAULT_OUTPUT_DIRECTORY = 'out'
DEFAULT_CONSTRUCTOR_POPULATION = 3
DEFAULT_EMPTY_POPULATION = 2

parser = ArgumentParser()
parser.add_argument('width', type=int, help='Width of the output image')
parser.add_argument('height', type=int, help='Height of the output image')
parser.add_argument('unit', type=int, help='Define the unit size')
parser.add_argument('--weight', default=DEFAULT_WEIGHT, type=int, help=f'Stroke weight. default {DEFAULT_WEIGHT}')
parser.add_argument('--out', default=DEFAULT_OUTPUT_DIRECTORY, type=Path, help=f'Director to dump images in. default {DEFAULT_OUTPUT_DIRECTORY}')
parser.add_argument('--month', default=DEFAULT_MONTH, help=f'Define month to select color palettes from. default {DEFAULT_MONTH}')
parser.add_argument('--N', default=DEFAULT_CONSTRUCTOR_POPULATION, type=int, help=f'Number of constructors to use. default {DEFAULT_CONSTRUCTOR_POPULATION}')
parser.add_argument('--empty', default=DEFAULT_EMPTY_POPULATION, type=int, help=f'Number of None objects to choose from at each step. default {DEFAULT_EMPTY_POPULATION}')
parser.add_argument('--a', default=-1, type=int)
parser.add_argument('--b', default=-1, type=int)

args = parser.parse_args()

output_dir = Path(args.out)
if not output_dir.exists():
    output_dir.mkdir()

constructor_set = [Rectangular_Prism, Triangular_Prism, Half_Triangular_Prism,
                   Half_Triangular_Prism_Mirror, Triangular_Prism_2, Tent,
                   Staple, Staple_2]

palettes = taisho_palette(args.month)


for a, palette in enumerate(palettes):
    mutes = list(permutations(palette, 3))
    for b, instance in enumerate(mutes):
        shuffle(constructor_set)
        constructor = constructor_set[:args.N]
        data = {
                'width': args.width,
                'height': args.height,
                'w': args.unit,
                'weight': args.weight,
                'bg': instance[0],
                'out': instance[1],
                'fill': instance[2]
            }
        data_inv = {
                'width': args.width,
                'height': args.height,
                'w': args.unit,
                'weight': args.weight,
                'bg': instance[0],
                'out': instance[2],
                'fill': instance[1]
            }
        image, draw = make_canvas(data)
        x_steps = args.width // args.unit
        x_off = (args.width - x_steps * args.unit) / 2
        y_steps = args.height // args.unit
        y_off = (args.height - y_steps * args.unit) / 2

        # adjust the emptyness ration
        objs = list(constructor) + [None for _ in range(args.empty)]
        x_idx = randint(0, x_steps - 1)
        y_idx = randint(0, y_steps - 1)
        for i in range(x_steps):
            x = (i * args.unit) + x_off
            for j in range(y_steps):
                y = (j * args.unit) + y_off
                if (f := choice(objs)) is None:
                    continue
                orient = choice(list(Orientation))
                f_obj = f(orient, x, y, args.unit)
                if x_idx == i and y_idx == j:
                    f_obj.draw(draw, data_inv)
                else:
                    f_obj.draw(draw, data)

        draw.flush()
        image.save(output_dir / f'{a}-{b}.png')
