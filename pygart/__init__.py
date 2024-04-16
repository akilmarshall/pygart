import tomllib
import datetime
from pathlib import Path

from PIL import Image
from aggdraw import Draw


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
