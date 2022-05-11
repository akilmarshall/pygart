'''
module to generate paths, sequences of 2 component vectors
'''
import numpy as np
from math import sqrt, cos, sin

def line(A, B, s):
    """
    linear path of s segments from A -> B
    """
    return np.linspace(A, B, s)

def ellipse(x:int, y:int, a:int, b:int, n:int, t:float, start:float=0.):
    """
    (x, y) path center
    (a, b) ellipse major,minor axis
    n      number of points in path
    t      offset in radians between points
    start  offset in radians from the major axis
    """
    theta = lambda i: start + (i * t)
    polar =  [(theta(i), (a * b) / sqrt((b * cos(theta(i)))**2 + (a * sin(theta(i)))**2)) for i in range(n)]
    return [(x + r * cos(angle), y + r * sin(angle)) for angle, r in polar]

def spiral(x:int, y:int, a:int, b:int, n:int, t:float, s:int, start:float=0.):
    """
    (x, y) path center
    (a, b) ellipse major,minor axis
    n      number of points in path
    t      offset in radians between points
    s      offset between points in the spiral (signiture describes direction)
    start  offset in radians from the major axis

    the ellipse function is a special case of this method when s = 0
    """
    theta = lambda i: start + (i * t)
    polar =  [(theta(i), (a * b) / sqrt((b * cos(theta(i)))**2 + (a * sin(theta(i)))**2)) for i in range(n)]
    polar = [(r, angle + s * i) for (i, (r, angle)) in enumerate(polar)] 
    return [(x + r * cos(angle), y + r * sin(angle)) for angle, r in polar]
