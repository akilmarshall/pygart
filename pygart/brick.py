"""
File: brick.py
Description: A module to assist in the drawing of "bricks" and things to do with bricks
"""

from PIL import ImageDraw


class Brick():

    """A class for drawing stylized rectangles"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def _pos(self, x: int, y: int):
        return (x, y, x + self.width, y + self.height)

    def __call__(self, canvas, x: int, y: int, color=None):
        if color: 
            ImageDraw.Draw(canvas.img).rectangle(self._pos(x, y), fill=color)
        else:
            ImageDraw.Draw(canvas.img).line(
                    [(x, y + self.height), (x + self.width, y + self.height)],
                    fill='grey',
                    width=2
                    )
            ImageDraw.Draw(canvas.img).line(
                    [(x + self.width, y), (x + self.width, y + self.height)],
                    fill='grey',
                    width=2
                    )
