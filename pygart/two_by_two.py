from aggdraw import Draw, Pen, Brush
from enum import Enum, auto
from random import choice
from abc import abstractmethod


class Orientation(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


ORIENTATIONS = list(Orientation)


def pick_orientation()-> Orientation:
    '''Select an orienation uniformly'''
    return choice(ORIENTATIONS)


class Grid_Base:
    def __init__(self, x, y, orienation: Orientation, data: dict, draw: Draw):
        self.data = data
        self.draw = draw
        self.orientation = orienation
        w = self.data['w']
        u = w / 2
        self.a = (x + 0, y + 0)
        self.b = (x + u, y + 0)
        self.c = (x + w, y + 0)
        self.d = (x + 0, y + u)
        self.e = (x + u, y + u)
        self.f = (x + w, y + u)
        self.g = (x + 0, y + w)
        self.h = (x + u, y + w)
        self.i = (x + w, y + w)

        self.pen = Pen(data['out'], data['weight'])
        self.brush = Brush(data['fill'])

        self.assemble()
        self.write()

        @abstractmethod
        def assemble(self):
            pass

        @abstractmethod
        def write(self):
            pass


class Half_Triangular_Prism(Grid_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assemble(self):
        s = self
        self.faces = {
                Orientation.NORTH: {
                        'top': (*s.b, *s.e, *s.g, *s.d),
                        'front': (*s.e, *s.g, *s.h),
                    }, 
                Orientation.SOUTH: {
                        'top': (*s.a, *s.e, *s.h, *s.d),
                        'front': (*s.a, *s.b, *s.e),
                    }, 
                Orientation.EAST: {
                        'top': (*s.a, *s.b, *s.f, *s.e),
                        'front': (*s.a, *s.e, *s.d),
                    }, 
                Orientation.WEST: {
                        'top': (*s.d, *s.e, *s.i, *s.h),
                        'front': (*s.e, *s.f, *s.i),
                    }, 
                }

    def write(self):
        s = self
        s.draw.polygon(s.faces[s.orientation]['top'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['front'], s.pen, s.brush)


class Half_Triangular_Prism_Mirror(Grid_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assemble(self):
        s = self
        self.faces = {
                Orientation.NORTH: {
                        'top': (*s.b, *s.f, *s.i, *s.e),
                        'front': (*s.e, *s.h, *s.i),
                    },
                Orientation.SOUTH: {
                        'top': (*s.e, *s.c, *s.f, *s.h),
                        'front': (*s.b, *s.c, *s.e),
                    },
                Orientation.EAST: {
                        'top': (*s.e, *s.f, *s.h, *s.g),
                        'front': (*s.d, *s.e, *s.g),
                    },
                Orientation.WEST: {
                        'top': (*s.b, *s.c, *s.e, *s.d),
                        'front': (*s.c, *s.e, *s.f),
                    },
                }

    def write(self):
        s = self
        s.draw.polygon(s.faces[s.orientation]['top'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['front'], s.pen, s.brush)


class Triangular_Prism(Grid_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assemble(self):
        s = self
        self.faces = {
                Orientation.NORTH: {
                        'front': (*s.e, *s.g, *s.i),
                        'left': (*s.b, *s.d, *s.g, *s.e),
                        'right': (*s.b, *s.f, *s.i, *s.e),
                    },
                Orientation.SOUTH: {
                        'front': (*s.a, *s.e, *s.c),
                        'left': (*s.a, *s.e, *s.h, *s.d),
                        'right': (*s.c, *s.e, *s.h, *s.f),
                    },
                Orientation.EAST: {
                        'front': (*s.a, *s.e, *s.g),
                        'left': (*s.a, *s.b, *s.f, *s.e),
                        'right': (*s.e, *s.f, *s.h, *s.g),
                    },
                Orientation.WEST: {
                        'front': (*s.e, *s.c, *s.i),
                        'left': (*s.d, *s.e, *s.i, *s.h),
                        'right': (*s.d, *s.e, *s.c, *s.b),
                    },
                }

    def write(self):
        s = self
        s.draw.polygon(s.faces[s.orientation]['front'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['left'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['right'], s.pen, s.brush)


class Rectangular_Prism(Grid_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assemble(self):
        s = self
        self.faces = {
                Orientation.NORTH: {
                    'front': (*s.d, *s.e, *s.h, *s.g),
                    'left': (*s.d, *s.e, *s.c, *s.b),
                    'right': (*s.e, *s.h, *s.f, *s.c),
                    },
                Orientation.SOUTH: {
                    'front': (*s.e, *s.f, *s.i, *s.h),
                    'left': (*s.a, *s.e, *s.h, *s.d),
                    'right': (*s.a, *s.b, *s.f, *s.e),
                    },
                Orientation.EAST: {
                    'front': (*s.a, *s.b, *s.e, *s.d),
                    'left': (*s.d, *s.e, *s.i, *s.h),
                    'right': (*s.b, *s.f, *s.i, *s.e),
                    },
                Orientation.WEST: {
                    'front': (*s.b, *s.c, *s.f, *s.e),
                    'left': (*s.d, *s.b, *s.e, *s.g),
                    'right': (*s.e, *s.f, *s.h, *s.g),
                    },
                }

    def write(self):
        s = self
        s.draw.polygon(s.faces[s.orientation]['front'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['left'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['right'], s.pen, s.brush)


class Triangular_Prism_2(Grid_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assemble(self):
        s = self
        self.faces = {
                    Orientation.NORTH: {
                        'front': (*s.d, *s.e, *s.h),
                        'left': (*s.d, *s.e, *s.c, *s.b),
                        'right': (*s.h, *s.e, *s.c, *s.f),
                        },
                    Orientation.SOUTH: {
                        'front': (*s.h, *s.e, *s.f),
                        'left': (*s.a, *s.d, *s.h, *s.e),
                        'right': (*s.a, *s.b, *s.f, *s.e),
                        },
                    Orientation.EAST: {
                        'front': (*s.d, *s.b, *s.e),
                        'left': (*s.d, *s.e, *s.i, *s.h),
                        'right': (*s.b, *s.f, *s.i, *s.e),
                        },
                    Orientation.WEST: {
                        'front': (*s.b, *s.e, *s.f),
                        'left': (*s.g, *s.d, *s.b, *s.e),
                        'right': (*s.e, *s.f, *s.h, *s.g),
                        },
                }

    def write(self):
        s = self
        s.draw.polygon(s.faces[s.orientation]['front'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['left'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['right'], s.pen, s.brush)


class Tent(Grid_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def assemble(self):
        s = self
        self.faces = {
                Orientation.NORTH: {
                    'left': (*s.d, *s.e, *s.c, *s.b),
                    'right': (*s.h, *s.e, *s.c, *s.f),
                    },
                Orientation.SOUTH: {
                    'left': (*s.a, *s.d, *s.h, *s.e),
                    'right': (*s.a, *s.b, *s.f, *s.e),
                    },
                Orientation.EAST: {
                    'left': (*s.d, *s.e, *s.i, *s.h),
                    'right': (*s.b, *s.f, *s.i, *s.e),
                    },
                Orientation.WEST: {
                    'left': (*s.g, *s.d, *s.b, *s.e),
                    'right': (*s.e, *s.f, *s.h, *s.g),
                    },
                }
    def write(self):
        s = self
        s.draw.polygon(s.faces[s.orientation]['left'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['right'], s.pen, s.brush)


class Staple(Grid_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def assemble(self):
        s = self
        self.faces = {
                Orientation.NORTH: {
                    'left': (*s.d, *s.e, *s.c, *s.b),
                    'right': (*s.h, *s.e, *s.c, *s.f),
                    'inside': (*s.g, *s.e, *s.h),
                    },
                Orientation.SOUTH: {
                    'left': (*s.a, *s.d, *s.h, *s.e),
                    'right': (*s.a, *s.b, *s.f, *s.e),
                    'inside': (*s.e, *s.h, *s.i),
                    },
                Orientation.EAST: {
                    'left': (*s.d, *s.e, *s.i, *s.h),
                    'right': (*s.b, *s.f, *s.i, *s.e),
                    'inside': (*s.a, *s.e, *s.d),
                    },
                Orientation.WEST: {
                    'left': (*s.g, *s.d, *s.b, *s.e),
                    'right': (*s.e, *s.f, *s.h, *s.g),
                    'inside': (*s.c, *s.e, *s.f),
                    },
                }

    def write(self):
        s = self
        s.draw.polygon(s.faces[s.orientation]['left'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['right'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['inside'], s.pen, s.brush)


class Staple_2(Grid_Base):
    '''for testing'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assemble(self):
        s = self
        self.faces = {
                Orientation.NORTH: {
                    'left': (*s.d, *s.e, *s.c, *s.b),
                    'right': (*s.h, *s.e, *s.c, *s.f),
                    'inside': (*s.g, *s.e, *s.d),
                    },
                Orientation.EAST: {
                    'left': (*s.d, *s.e, *s.i, *s.h),
                    'right': (*s.b, *s.f, *s.i, *s.e),
                    'inside': (*s.a, *s.e, *s.b),
                    },
                Orientation.WEST: {
                    'left': (*s.g, *s.d, *s.b, *s.e),
                    'right': (*s.e, *s.f, *s.h, *s.g),
                    'inside': (*s.c, *s.e, *s.b),
                    },
                Orientation.SOUTH: {
                    'left': (*s.a, *s.d, *s.h, *s.e),
                    'right': (*s.a, *s.b, *s.f, *s.e),
                    'inside': (*s.e, *s.f, *s.i),
                    },
                }

    def write(self):
        s = self
        s.draw.polygon(s.faces[s.orientation]['left'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['right'], s.pen, s.brush)
        s.draw.polygon(s.faces[s.orientation]['inside'], s.pen, s.brush)
