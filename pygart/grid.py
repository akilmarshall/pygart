from itertools import product

# -> Generator[tuple[float, float]

def Aligned(m, n, width, height, x_off=0, y_off=0, center=False):
    '''
    Produce an aligned grid of (m, n) objects onto the (data.width, data.height) area
    '''
    x_step = width / m
    y_step = height / n
    x_gap = x_step * 
    for i, j in product(range(m), range(n)):
        x = i * x_step + x_off
        y = j * y_step + y_off
        yield x, y

