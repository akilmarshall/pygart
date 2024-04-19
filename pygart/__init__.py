import tomllib
import datetime
from pathlib import Path

from PIL import Image
from aggdraw import Draw
from enum import Enum, auto


TAISHO_DATA = None
with open(Path(__file__).parent / 'taisho-showa.toml', 'rb') as f:
    TAISHO_DATA = tomllib.load(f)


def taisho_color_to_rgb(color: str):
    return tuple(TAISHO_DATA['color'][color])


def taisho_palette(month: str):
    for palette in TAISHO_DATA['palette'][month]:
        yield [taisho_color_to_rgb(p) for p in palette]


def make_canvas(data: dict) -> tuple[Image.Image, Draw]:
    img = Image.new('RGB', (data['width'], data['height']), color=data['bg'])
    return img, Draw(img)


def current_month():
    # Get the current month as an integer
    current_month = datetime.datetime.now().month

    # Convert the month integer to its corresponding name
    month_name = datetime.date(1900, current_month, 1).strftime('%B').lower()

    return month_name


SOLARIZED_COLORS: list[str] = ['base03', 'base02', 'base01', 'base00', 'base0',
                               'base1', 'base2', 'base3', 'yellow', 'orange',
                               'red', 'magenta', 'violet', 'blue', 'cyan',
                               'green']

class Color_Type(Enum):
    ANY = auto()
    BG_LIGHT = auto()
    BG_DARK = auto()
    COLOR = auto()


SOLARIZED_DATA = None
with open(Path(__file__).parent / 'solarized.toml', 'rb') as f:
    SOLARIZED_DATA = tomllib.load(f)


def solarized_color(color: str) -> tuple[int, int, int]:
    return tuple(SOLARIZED_DATA['color'][color])


def solarized_colors(selection: Color_Type, string=False):
    def _map(i, j):
        if string:
            return SOLARIZED_COLORS[i:j]
        return list(map(solarized_color, SOLARIZED_COLORS[i:j]))

    match selection:
        case Color_Type.ANY:
            return _map(0, 16)
        case Color_Type.BG_LIGHT:
            return _map(4, 8)
        case Color_Type.BG_DARK:
            return _map(0, 4)
        case Color_Type.COLOR:
            return _map(8, 16)
