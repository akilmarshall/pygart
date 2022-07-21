"""
File: canvas.py
Description: A module providing a wrapper for PIL.Image to
             allow/facilitate image rendering
"""

from PIL import Image

from .color import RGBA, solarized


__all__ = ['Canvas']


class Canvas:
    '''
    Wrapper class for PIL.Image
    '''

    def __init__(
            self,
            width: int,
            height: int,
            path: str = 'out.png',
            color: tuple[int, int, int] | None = None
            ):
        self.width = width
        self.height = height
        self.path = path
        self.color = RGBA(solarized['base3']) if color is None else color

        self._setup()

    def _setup(self):
        self.img = Image.new(
            'RGBA', (self.width, self.height), color=self.color)

    def save(self, fname=None):
        if fname:
            self.img.save(fname)
        else:
            self.img.save(self.path)
