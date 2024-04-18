from itertools import product


def Aligned(m: int, n: int, width: int, height: int, x_off:int=0, y_off:int=0):
    '''
    Produce an aligned grid of (m, n) objects onto the (width, height) area
    '''
    x_step = width / m
    y_step = height / n
    for i, j in product(range(m), range(n)):
        x = i * x_step + x_off
        y = j * y_step + y_off
        yield x, y

