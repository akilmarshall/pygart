from aggdraw import Draw, Pen, Brush
from enum import Enum, auto
from random import choice


class Orientation(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


ORIENTATIONS = list(Orientation)


def pick_orientation()-> Orientation:
    '''Select an orienation uniformly'''
    return choice(ORIENTATIONS)


class Grid_Base_2:
    def __init__(self, x, y, data):
        self.data = data
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


class Grid_Base:

    def __init__(self, x, y, w):
        u = w / 2  # w is a "double" u after all :)
        self.w = w
        self.u = u
        self.a = (x + 0, y + 0)
        self.b = (x + u, y + 0)
        self.c = (x + w, y + 0)
        self.d = (x + 0, y + u)
        self.e = (x + u, y + u)
        self.f = (x + w, y + u)
        self.g = (x + 0, y + w)
        self.h = (x + u, y + w)
        self.i = (x + w, y + w)


class Half_Triangular_Prism(Grid_Base):
    def __init__(self, orient: Orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orient = orient

    def draw(self, draw: Draw, data: dict):
        s = self
        pen = Pen(data['out'], data['weight'])
        brush = Brush(data['fill'])

        match s.orient:
            case Orientation.NORTH:
                # draw top
                draw.polygon((*s.b, *s.e, *s.g, *s.d), pen, brush)
                # draw front
                draw.polygon((*s.e, *s.g, *s.h), pen, brush)
            case Orientation.SOUTH:
                # draw top
                draw.polygon((*s.a, *s.e, *s.h, *s.d), pen, brush)
                # draw front
                draw.polygon((*s.a, *s.b, *s.e), pen, brush)
            case Orientation.EAST:
                # draw top
                draw.polygon((*s.a, *s.b, *s.f, *s.e), pen, brush)
                # draw front
                draw.polygon((*s.a, *s.e, *s.d), pen, brush)
            case Orientation.WEST:
                # draw top
                draw.polygon((*s.d, *s.e, *s.i, *s.h), pen, brush)
                # draw front
                draw.polygon((*s.e, *s.f, *s.i), pen, brush)


class Half_Triangular_Prism_Mirror(Grid_Base):
    def __init__(self, orient: Orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orient = orient

    def draw(self, draw: Draw, data: dict):
        s = self
        pen = Pen(data['out'], data['weight'])
        brush = Brush(data['fill'])

        match s.orient:
            case Orientation.NORTH:
                # draw top
                draw.polygon((*s.b, *s.f, *s.i, *s.e), pen, brush)
                # draw front
                draw.polygon((*s.e, *s.h, *s.i), pen, brush)
            case Orientation.SOUTH:
                # draw top
                draw.polygon((*s.e, *s.c, *s.f, *s.h), pen, brush)
                # draw front
                draw.polygon((*s.b, *s.c, *s.e), pen, brush)
            case Orientation.EAST:
                # draw top
                draw.polygon((*s.e, *s.f, *s.h, *s.g), pen, brush)
                # draw front
                draw.polygon((*s.d, *s.e, *s.g), pen, brush)
            case Orientation.WEST:
                # draw top
                draw.polygon((*s.b, *s.c, *s.e, *s.d), pen, brush)
                # draw front
                draw.polygon((*s.c, *s.e, *s.f), pen, brush)


class Triangular_Prism(Grid_Base):
    def __init__(self, orient: Orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orient = orient

    def draw(self, draw: Draw, data: dict):
        s = self
        pen = Pen(data['out'], data['weight'])
        brush = Brush(data['fill'])

        match s.orient:
            case Orientation.NORTH:
                # draw front
                draw.polygon((*s.e, *s.g, *s.i), pen, brush)
                # draw left
                draw.polygon((*s.b, *s.d, *s.g, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.b, *s.f, *s.i, *s.e), pen, brush)
            case Orientation.SOUTH:
                # draw front
                draw.polygon((*s.a, *s.e, *s.c), pen, brush)
                # draw left
                draw.polygon((*s.a, *s.e, *s.h, *s.d), pen, brush)
                # draw right
                draw.polygon((*s.c, *s.e, *s.h, *s.f), pen, brush)
            case Orientation.EAST:
                # draw front
                draw.polygon((*s.a, *s.e, *s.g), pen, brush)
                # draw left
                draw.polygon((*s.a, *s.b, *s.f, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.e, *s.f, *s.h, *s.g), pen, brush)
            case Orientation.WEST:
                # draw front
                draw.polygon((*s.e, *s.c, *s.i), pen, brush)
                # draw left
                draw.polygon((*s.d, *s.e, *s.i, *s.h), pen, brush)
                # draw right
                draw.polygon((*s.d, *s.e, *s.c, *s.b), pen, brush)


class Rectangular_Prism(Grid_Base):
    def __init__(self, orient: Orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orient = orient

    def draw(self, draw: Draw, data: dict):
        s = self
        pen = Pen(data['out'], data['weight'])
        brush = Brush(data['fill'])

        match s.orient:
            case Orientation.NORTH:
                # draw front
                draw.polygon((*s.d, *s.e, *s.h, *s.g), pen, brush)
                # draw left
                draw.polygon((*s.d, *s.e, *s.c, *s.b), pen, brush)
                # draw right
                draw.polygon((*s.e, *s.h, *s.f, *s.c), pen, brush)
            case Orientation.SOUTH:
                # draw front
                draw.polygon((*s.e, *s.f, *s.i, *s.h), pen, brush)
                # draw left
                draw.polygon((*s.a, *s.e, *s.h, *s.d), pen, brush)
                # draw right
                draw.polygon((*s.a, *s.b, *s.f, *s.e), pen, brush)
            case Orientation.EAST:
                # draw front
                draw.polygon((*s.a, *s.b, *s.e, *s.d), pen, brush)
                # draw left
                draw.polygon((*s.d, *s.e, *s.i, *s.h), pen, brush)
                # draw right
                draw.polygon((*s.b, *s.f, *s.i, *s.e), pen, brush)
            case Orientation.WEST:
                # draw front
                draw.polygon((*s.b, *s.c, *s.f, *s.e), pen, brush)
                # draw left
                draw.polygon((*s.d, *s.b, *s.e, *s.g), pen, brush)
                # draw right
                draw.polygon((*s.e, *s.f, *s.h, *s.g), pen, brush)


class Triangular_Prism_2(Grid_Base):
    def __init__(self, orient: Orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orient = orient

    def draw(self, draw: Draw, data: dict):
        s = self
        pen = Pen(data['out'], data['weight'])
        brush = Brush(data['fill'])

        match s.orient:
            case Orientation.NORTH:
                # draw front
                draw.polygon((*s.d, *s.e, *s.h), pen, brush)
                # draw left
                draw.polygon((*s.d, *s.e, *s.c, *s.b), pen, brush)
                # draw right
                draw.polygon((*s.h, *s.e, *s.c, *s.f), pen, brush)
            case Orientation.SOUTH:
                # draw front
                draw.polygon((*s.h, *s.e, *s.f), pen, brush)
                # draw left
                draw.polygon((*s.a, *s.d, *s.h, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.a, *s.b, *s.f, *s.e), pen, brush)
            case Orientation.EAST:
                # draw front
                draw.polygon((*s.d, *s.b, *s.e), pen, brush)
                # draw left
                draw.polygon((*s.d, *s.e, *s.i, *s.h), pen, brush)
                # draw right
                draw.polygon((*s.b, *s.f, *s.i, *s.e), pen, brush)
            case Orientation.WEST:
                # draw front
                draw.polygon((*s.b, *s.e, *s.f), pen, brush)
                # draw left
                draw.polygon((*s.g, *s.d, *s.b, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.e, *s.f, *s.h, *s.g), pen, brush)


class Tent(Grid_Base):
    def __init__(self, orient: Orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orient = orient

    def draw(self, draw: Draw, data: dict):
        s = self
        pen = Pen(data['out'], data['weight'])
        brush = Brush(data['fill'])

        match s.orient:
            case Orientation.NORTH:
                # draw left
                draw.polygon((*s.d, *s.e, *s.c, *s.b), pen, brush)
                # draw right
                draw.polygon((*s.h, *s.e, *s.c, *s.f), pen, brush)
            case Orientation.SOUTH:
                # draw left
                draw.polygon((*s.a, *s.d, *s.h, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.a, *s.b, *s.f, *s.e), pen, brush)
            case Orientation.EAST:
                # draw left
                draw.polygon((*s.d, *s.e, *s.i, *s.h), pen, brush)
                # draw right
                draw.polygon((*s.b, *s.f, *s.i, *s.e), pen, brush)
            case Orientation.WEST:
                # draw left
                draw.polygon((*s.g, *s.d, *s.b, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.e, *s.f, *s.h, *s.g), pen, brush)


class Staple(Grid_Base):
    def __init__(self, orient: Orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orient = orient

    def draw(self, draw: Draw, data: dict):
        s = self
        pen = Pen(data['out'], data['weight'])
        brush = Brush(data['fill'])

        match s.orient:
            case Orientation.NORTH:
                # draw left
                draw.polygon((*s.d, *s.e, *s.c, *s.b), pen, brush)
                # draw right
                draw.polygon((*s.h, *s.e, *s.c, *s.f), pen, brush)
                # inside
                draw.polygon((*s.g, *s.e, *s.h), pen, brush)
            case Orientation.SOUTH:
                # draw left
                draw.polygon((*s.a, *s.d, *s.h, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.a, *s.b, *s.f, *s.e), pen, brush)
                # inside
                draw.polygon((*s.e, *s.h, *s.i), pen, brush)
            case Orientation.EAST:
                # draw left
                draw.polygon((*s.d, *s.e, *s.i, *s.h), pen, brush)
                # draw right
                draw.polygon((*s.b, *s.f, *s.i, *s.e), pen, brush)
                # inside
                draw.polygon((*s.a, *s.e, *s.d), pen, brush)
            case Orientation.WEST:
                # draw left
                draw.polygon((*s.g, *s.d, *s.b, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.e, *s.f, *s.h, *s.g), pen, brush)
                # inside
                draw.polygon((*s.c, *s.e, *s.f), pen, brush)


class Staple_2(Grid_Base):
    def __init__(self, orient: Orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orient = orient

    def draw(self, draw: Draw, data: dict):
        s = self
        pen = Pen(data['out'], data['weight'])
        brush = Brush(data['fill'])

        match s.orient:
            case Orientation.NORTH:
                # draw left
                draw.polygon((*s.d, *s.e, *s.c, *s.b), pen, brush)
                # draw right
                draw.polygon((*s.h, *s.e, *s.c, *s.f), pen, brush)
                # inside
                draw.polygon((*s.g, *s.e, *s.d), pen, brush)
            case Orientation.SOUTH:
                # draw left
                draw.polygon((*s.a, *s.d, *s.h, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.a, *s.b, *s.f, *s.e), pen, brush)
                # inside
                draw.polygon((*s.e, *s.f, *s.i), pen, brush)
            case Orientation.EAST:
                # draw left
                draw.polygon((*s.d, *s.e, *s.i, *s.h), pen, brush)
                # draw right
                draw.polygon((*s.b, *s.f, *s.i, *s.e), pen, brush)
                # inside
                draw.polygon((*s.a, *s.e, *s.b), pen, brush)
            case Orientation.WEST:
                # draw left
                draw.polygon((*s.g, *s.d, *s.b, *s.e), pen, brush)
                # draw right
                draw.polygon((*s.e, *s.f, *s.h, *s.g), pen, brush)
                # inside
                draw.polygon((*s.c, *s.e, *s.b), pen, brush)


class Staple_3(Grid_Base_2):
    '''for testing'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assemble(self, draw, left: tuple, right:tuple, inside:tuple):
        # draw left
        draw.polygon(left, self.pen, self.brush)
        # draw right
        draw.polygon(right, self.pen, self.brush)
        # inside
        draw.polygon(inside, self.pen, self.brush)

    def draw(self, orientation: Orientation, draw: Draw):
        s = self
        match orientation:
            case Orientation.NORTH:
                self.assemble(
                        draw,
                        (*s.d, *s.e, *s.c, *s.b),
                        (*s.h, *s.e, *s.c, *s.f),
                        (*s.g, *s.e, *s.d))
            case Orientation.SOUTH:
                self.assemble(
                        draw,
                        (*s.a, *s.d, *s.h, *s.e),
                        (*s.a, *s.b, *s.f, *s.e),
                        (*s.e, *s.f, *s.i))
            case Orientation.EAST:
                self.assemble(
                        draw,
                        (*s.d, *s.e, *s.i, *s.h),
                        (*s.b, *s.f, *s.i, *s.e),
                        (*s.a, *s.e, *s.b))
            case Orientation.WEST:
                self.assemble(
                        draw,
                        (*s.g, *s.d, *s.b, *s.e),
                        (*s.e, *s.f, *s.h, *s.g),
                        (*s.c, *s.e, *s.b))
