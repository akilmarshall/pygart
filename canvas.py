from color import *
from PIL import Image


class Canvas:
    '''
    Wrapper class for PIL.Image
    '''

    def __init__(self, width: int, height: int, color: tuple[int, int, int] | None = None):
        self.width = width
        self.height = height
        self.color = RGBA(base3) if color is None else color

        self._setup()

    def _setup(self):
        self.img = Image.new(
            'RGBA', (self.width, self.height), color=self.color)

    def save(self, fname: str = 'out.png'):
        self.img.save(fname)
