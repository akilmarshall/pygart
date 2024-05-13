from random import random
from typing import Callable
from itertools import product

class MList(list):
    '''
    Modulo list.
    A normal python list except that access via [idx] is mapped by (idx % len(self))
    i.e. the end of the list is "glued" to the front by modulus of the length
    '''
    def __getitem__(self, idx):
        if len(self) > 0:
            return super().__getitem__(idx % len(self))
        else:
            return super().__getitem__(idx)

    def __setitem__(self, idx, item):
        if len(self) > 0:
            super().__setitem__(idx % len(self), item)
        else:
            super().__setitem__(idx, item)


class MGrid:
    '''Modulo grid'''
    def __init__(self, columns: int, rows: int, f: Callable[[], int]):
        self.columns = columns
        self.rows = rows
        self.state = self.make_grid(columns, rows, f)

    def make_grid(self, columns: int, rows: int, f: Callable[[], int]) -> list[list[int]]:
        grid = MList([])
        for _ in range(columns):
            grid.append(MList([f() for _ in range(rows)]))
        return grid

    def pprint(self):
        for j in range(self.rows): 
            for i in range(self.columns):
                print(self[i][j], end='\t')
            print()

    def get(self, xy: tuple[int, int]):
        x, y = xy
        return self.state

    def __getitem__(self, idx):
        return self.state[idx]

    def __len__(self):
        return len(self.state)

    def sub_grid(self, xy: tuple[int, int], w: int, h: int, x_off:int=0, y_off:int=0):
        '''
        The subgrid is rooted at (x, y) with a width of w and a height of h
        It may be offset with (x_off, y_off)
        '''
        x, y = xy
        sub = MGrid(w, h, lambda: 0)
        for i, j in product(range(w), range(h)):
            sub[i][j] = self[x + i + x_off][y + j + y_off]
        return sub


class GOL:
    def __init__(self, columns: int, rows: int, initial_state:None|MGrid=None, w:float=0.5):
        self.columns = columns
        self.rows = rows
        if initial_state is None:
            life_choice = lambda: 0 if random() <= w else 1
            self.state = MGrid(columns, rows, life_choice)
        else:
            self.state = initial_state
            self.rows = len(initial_state)
            self.columns = len(initial_state[0])

    def step(self):
        old = self.state
        self.state = MGrid(self.columns, self.rows, lambda: 0)
        for i, j in product(range(self.columns), range(self.rows)):
            hood = old.sub_grid((i, j), 3, 3, x_off=-1, y_off=-1)
            alive = sum(map(sum, hood.state)) - old[i][j]
            if old[i][j]:
                if alive < 2 or alive > 3:
                    # die
                    self.state[i][j] = 0
            else:
                if alive == 3:
                    # revive
                    self.state[i][j] = 1
