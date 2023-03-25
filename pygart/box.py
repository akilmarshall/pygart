__all__ = ['box']

from pygart.extra import V


def sub(x, y, a, handedness=True, invert=False):
    '''
    General function to compute the points of the sub parts of a 3 part box.
    :handedness: True -> right, False -> left
    :invert: True -> flip, False -> normal
    '''
    root = V(x, y)
    b = a / 2
    if invert:
        if handedness:
            # Right
            yield (root + V(0, -b))()  # A
            yield (root + V(0, -a))()  # B
            yield (root + V(-b, -b))()  # C
            yield (root + V(-b, 0))()   # D
        else:
            # Left
            yield (root + V(0, -b))()  # A
            yield (root + V(0, -a))()  # B
            yield (root + V(b, -b))()  # C
            yield (root + V(b, 0))()   # D
    else:
        if handedness:
            # Right
            yield (root + V(0, b))()  # A
            yield (root + V(0, a))()  # B
            yield (root + V(b, b))()  # C
            yield (root + V(b, 0))()   # D
        else:
            # Left
            yield (root + V(0, b))()  # A
            yield (root + V(0, a))()  # B
            yield (root + V(-b, b))()  # C
            yield (root + V(-b, 0))()   # D


def left(x, y, a):
    '''
    Left part normal at (x, y) size a
    '''
    return sub(x, y, a, handedness=False)


def right(x, y, a):
    '''
    Right part normal at (x, y) size a
    '''
    return sub(x, y, a)


def left_inverted(x, y, a):
    '''
    Left part inverted at (x, y) size a
    '''
    return sub(x, y, a, handedness=False, invert=True)


def right_inverted(x, y, a):
    '''
    Right part inverted at (x, y) size a
    '''
    return sub(x, y, a, invert=True)


def main(x, y, a):
    b = a / 2
    root = V(x, y)
    yield (root + V(0, b))()   # A
    yield (root + V(b, 0))()   # B
    yield (root + V(0, -b))()  # C
    yield (root + V(-b, 0))()  # D


def box(x, y, a, flip=False):
    '''
    Compute a Box at (x, y) with size a.
    Return a list of the sub parts : [main, left, right]
    '''
    if flip:
        return [list(part(x, y, a)) for part in [main, left_inverted, right_inverted]]

    return [list(part(x, y, a)) for part in [main, left, right]]
