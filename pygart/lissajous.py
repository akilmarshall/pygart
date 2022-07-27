from math import sin, pi


__all__ = ['Lissajous']


class Lissajous:
    '''
    Lissajous curve in the plane
    X(t) = A * sin(a * t + delta)
    Y(t) = B * sin(b * t)
    '''

    def __init__(self, A, B, a, b, delta, x: int = 0, y: int = 0, n: int = 1000):
        """
        Curve parameters
        :A:     absolute magnitude of the x coordinate
        :B:     absolute magnitude of the y coordinate
        :a:     "stretch" of the x coordinates wave form
        :b:     "stretch" of the x coordinates wave form
        :delta: time offset of the x coordinate wave form (pi / 2) is cos
        :x:     x center or offset of the curve in the plane
        :y:     y center or offset of the curve in the plane
        :n:     number of points used to represent the curve when iterated
        """

        self.A = A
        self.B = B
        self.a = a
        self.b = b
        self.delta = delta
        self.x_offset = x
        self.y_offset = y

        self._t = 0
        self._stop_iter = False
        self._n = n

    def x(self, t):
        '''A * sin(a * t + delta) '''
        return self.A * sin(self.a * t + self.delta) + self.x_offset

    def y(self, t):
        '''B * sin(b * t) '''
        return self.B * sin(self.b * t) + self.y_offset

    def __call__(self, t):
        """ Periodic in [0, 2pi). Continuous. """
        return (self.x(t), self.y(t))

    def set_A(self, A):
        """Builder style method to update A. """
        self.A = A
        return self

    def set_B(self, B):
        """Builder style method to update B. """
        self.B = B
        return self

    def set_a(self, a):
        """Builder style method to update a. """
        self.a = a
        return self

    def set_b(self, b):
        """Builder style method to update b. """
        self.b = b
        return self

    def set_delta(self, delta):
        """Builder style method to update delta. """
        self.delta = delta
        return self

    def set_offset_x(self, x):
        """Builder style method to update x (offset). """
        self.x_offset = x
        return self

    def set_offset_y(self, y):
        """Builder style method to update y (offset). """
        self.y_offset = y
        return self

    def set_offset(self, offset: tuple[int, int]):
        """Builder style method to update the offset (as a tuple). """
        x, y = offset
        return self.set_offset_x(x).set_offset_y(y)

    def set_n(self, offset: tuple[int, int]):
        """
            Builder style method to update the number of points used to
            represent the curve (when iterating).
        """
        x, y = offset
        return self.set_offset_x(x).set_offset_y(y)

    def __iter__(self):
        while not self._stop_iter:
            yield self(2 * pi * self._t / self._n)
            self._t += 1
            if self._t >= self._n:
                self._stop_iter = True
        self._t = 0
        self._stop_iter = False
