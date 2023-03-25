__all__ = ['V']
import operator
from functools import reduce
from itertools import repeat


class V:
    """
    A wrapper class for tuples of arbitrary length.
    Makes liberal use of map and the operator functions.
    The members of these tuples must support
    Supports:
        add
        subtract
        scalar multiply
        scalar floordivision
        scalar trudivision
        negation
    """

    def __init__(self, *args, **keyargs):
        self.p = args
        self.n = len(args)

    def v(self) -> tuple[float, float]:
        '''Maps int over tuple elements and returns tuple. '''
        return tuple(map(int, self.p))

    def _compatibility(self, other):
        if self.n != other.n:
            err_msg = f'Tuple length mismatch. {self} mismatch with {other}'
            raise TypeError(err_msg)

    def __add__(self, other):
        self._compatibility(other)

        return V(*list(map(lambda x: operator.add(*x), zip(self.p, other.p))))

    def __sub__(self, other):
        self._compatibility(other)

        return V(*list(map(lambda x: operator.sub(*x), zip(self.p, other.p))))

    def __mul__(self, s):
        '''Left scalar multiplication: s * x for each element. '''
        return V(*list(map(lambda x: operator.mul(*x), zip(repeat(s), self.p))))

    def __call__(self):
        return self.v()

    def __repr__(self):
        return f'V({", ".join(map(str, self.p))})'

    def __rmul__(self, s):
        '''Right scalar multiplication x * s for each element. '''
        return V(*list(map(lambda x: operator.mul(*x), zip(self.p, repeat(s)))))

    def __eq__(self, other):
        '''Map operator.eq over each match pair of elements. '''
        self._compatibility(other)

        return reduce(operator.and_, map(lambda x: operator.eq(*x), zip(self.p, other.p)))

    def __floordiv__(self, d):
        '''Floor divide each element by d, x // d. '''
        return V(*list(map(lambda x: operator.floordiv(*x), zip(self.p, repeat(d)))))

    def __truediv__(self, d):
        '''Divide each element by d in self.p, x / d. '''
        return V(*list(map(lambda x: operator.truediv(*x), zip(self.p, repeat(d)))))

    def __neg__(self):
        '''Map operator.neg over each element. '''
        return V(*list(map(operator.neg, self.p)))
