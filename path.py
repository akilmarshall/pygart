'''
module to generate paths, sequences of 2 component vectors
'''
from math import dist, atan, cos, sin

def line(A:tuple[int, int], B:tuple[int, int], s:int):
    """
    linear path of s segments from A -> B
    """
    ax, ay = A
    bx, by = B
    m = dist(A, B) / s
    theta = atan((by - ay) /(bx - ax))
    dx = m * cos(theta)
    dy = m * sin(theta)

    return [(ax + dx*i, ay + dy*i) for i in range(s + 1)]
