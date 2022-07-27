from math import sin, pi


__all__ = ['Lissajous']

class Lissajous:
    '''
    Lissajous curve in the plane
    X(t) = A * sin(a * t + delta)
    Y(t) = B * sin(b * t)
    '''

    def __init__(self, A, B, a, b, delta, x: int = 0, y: int = 0):
        self.A = A
        self.B = B
        self.a = a
        self.b = b
        self.delta = delta
        self.x_offset = x
        self.y_offset = y

    def x(self, t):
        '''A * sin(a * t + delta) '''
        return self.A * sin(self.a * t + self.delta) + self.x_offset

    def y(self, t):
        '''B * sin(b * t) '''
        return self.B * sin(self.b * t) + self.y_offset

    def __call__(self, t):
        ''' Periodic in [0, 2pi). Continuous. '''
        return (self.x(t), self.y(t))
