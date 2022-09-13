from math import sqrt, cos, sin, pi
from pygart import V

# TODO:
# draw the quad trees
# currently the trees are over ID-less points (indistinguisable)
# extend the implementation (make a new product type with V and an id type) that the tree understands


class AABB:
    def __init__(self, xy: V, size: V):
        self.xy = xy        # center
        self.size = size    # half dimensions

    def actA(self):
        """Return the action to move self.xy to the center of the A child. """
        return  0.5 * V(self.size.x, -self.size.y)

    def actB(self):
        """Return the action to move self.xy to the center of the B child. """
        return 0.5 * V(-self.size.x, -self.size.y)

    def actC(self):
        """Return the action to move self.xy to the center of the C child. """
        return 0.5 * V(-self.size.x, self.size.y)

    def actD(self):
        """Return the action to move self.xy to the center of the D child. """
        return 0.5 * V(self.size.x, -self.size.y)

    def __contains__(self, xy: V):
        x = self.xy.x - self.size.x <= xy.x <= self.xy.x + self.size.x
        y = self.xy.y - self.size.y <= xy.y <= self.xy.y + self.size.y
        return x and y

    def overlap(self, other):
        a = other.xy + 2 * self.actA()
        b = other.xy + 2 * self.actB()
        c = other.xy + 2 * self.actC()
        d = other.xy + 2 * self.actD()

        return a in self or b in self or c in self or d in self
    def __repr__(self):
        return f'AABB({self.xy}, {self.size})'


class QuadTree:
    """
    .___.
    |B|A|
    |---|
    |C|D|
     ----
    """
    def __init__(self, boundary: AABB, cap=4):
        self.boundary = boundary
        self.cap = cap

        self.points = []
        self.A = None
        self.B = None
        self.C = None
        self.D = None

    def insert(self, xy: V):
        """Insert a point into the proper subtree, splitting if necessary. """
        if xy not in self.boundary:
            return False
        if len(self.points) < self.cap:
            self.points.append(xy)
        else:
            if not self.A:
                self.subdivide()
            if self.A.insert(xy):
                pass
            elif self.B.insert(xy):
                pass
            elif self.C.insert(xy):
                pass
            elif self.D.insert(xy):
                pass

        return True

    def query_range(self, region: AABB):
        found = []
        if self.boundary.overlap(region):
            for p in self.points:
                if p in region:
                    found.append(p)
            if self.A is not None:
                for p in self.A.query_range(region):
                    found.append(p)
                for p in self.B.query_range(region):
                    found.append(p)
                for p in self.C.query_range(region):
                    found.append(p)
                for p in self.D.query_range(region):
                    found.append(p)
        return found

    def subdivide(self):
        self.A = QuadTree(AABB(self.boundary.xy + self.boundary.actA(), 0.5 * self.boundary.size))
        self.B = QuadTree(AABB(self.boundary.xy + self.boundary.actB(), 0.5 * self.boundary.size))
        self.C = QuadTree(AABB(self.boundary.xy + self.boundary.actC(), 0.5 * self.boundary.size))
        self.D = QuadTree(AABB(self.boundary.xy + self.boundary.actD(), 0.5 * self.boundary.size))

    def __repr__(self):
        return f'QuadTree({self.boundary}){self.points} -> [{self.A} {self.B} {self.C} {self.D}]'

    def __contains__(self, xy: V) -> bool:
        return xy in self.boundary



p = V(250, 250)

a = V(10, 10)
b = V(10, 240)
c = V(10, 510)

tree = QuadTree(AABB(p, p))
