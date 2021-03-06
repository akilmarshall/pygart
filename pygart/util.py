"""
File: util.py
Description: Utility module, universal/odd functions and classes belong here
"""

from sys import argv


def info():
    if len(argv) != 4:
        print("usage: width heigh <path>.png")
        print(f"got {argv}")
        quit()
    _, width, height, path = argv
    return int(width), int(height), path
