from random import random, choice
from typing import Callable
from itertools import product

class MList(list):
    '''
    Modulo list.
    A normal python list except that access via [idx] is mapped by (idx % len(self))
    i.e. the end of the list is "glued" to the front by modulus of the length
    '''
    NEIGHBOR_COORDINATES = [-1, 1]

    def neighbors(self, n):
        for d in MList.NEIGHBOR_COORDINATES:
            yield n + d, self[n + d]

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

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True


class MGrid:
    '''Modulo grid'''
    NEIGHBOR_COORDINATES = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def __init__(self, columns: int, rows: int, f: Callable[[], int]):
        self.columns = columns
        self.rows = rows
        self.state = self.make_grid(columns, rows, f)

    def full(self):
        for x in range(self.columns):
            for y in range(self.rows):
                if self.state[x][y] == 0:
                    return False

        return True

    def empty_spaces(self):
        empty_pop = 0
        for x in range(self.columns):
            for y in range(self.rows):
                if self.state[x][y] == 0:
                    empty_pop += 1

        return empty_pop

    def neighbors(self, x, y):
        for n, m in MGrid.NEIGHBOR_COORDINATES:
            yield x + n, y + m, self[x + n][y + m]

    def __eq__(self, other):
        if self.columns != other.columns:
            return False
        if self.rows != other.rows:
            return False
        for i, j in product(range(self.columns), range(self.rows)):
            if self.state[i][j] != other.state[i][j]:
                return False
        return True

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

    def points(self):
        for i, j in product(range(self.columns), range(self.rows)):
            yield i, j

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
    
    def population(self, skip:None|tuple[int, int]=None):
        pop =  sum(map(sum, self.state))
        if skip:
            x, y = skip
            return pop - self.state[x][y]
        return pop

    def occupancy(self, skip:None|tuple[int, int]=None):
        def row_occupy(row):
            pop = 0
            for x in row:
                if x > 0:
                    pop += 1
            return pop
        quant = sum(map(row_occupy, self.state))
        if skip:
            x, y = skip
            return quant - 1 if self.state[x][y] > 0 else 0

        return quant

    def image(self):
        ''' if cell => 1 change to 1.'''
        img = MGrid(self.columns, self.rows, lambda: 0)
        for i, j in self.points():
            img[i][j] = 1 if self.state[i][j] >= 1 else 0
        return img

    def decay(self):
        for i, j in self.points():
            if self.state[i][j] > 0:
                self.state[i][j] -= 1

class gol_base:
    def dead(self):
        return 0 == sum(map(sum, self.grid.state))

    def step(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        if not self.dead():
            self.step()
            return self.grid

        raise StopIteration()

    def pprint(self):
        self.grid.pprint()

    def __eq__(self, other):
        return self.grid == other.grid


class GOL(gol_base):
    def __init__(self, columns: int, rows: int, initial_state:None|MGrid=None, w:float=0.5):
        self.columns = columns
        self.rows = rows
        if initial_state is None:
            life_choice = lambda: 0 if random() <= w else 1
            self.grid = MGrid(columns, rows, life_choice)
        else:
            self.grid = initial_state
            self.rows = len(initial_state)
            self.columns = len(initial_state[0])

    def step(self):
        old = self.grid
        self.grid = MGrid(self.columns, self.rows, lambda: 0)
        for i, j in product(range(self.columns), range(self.rows)):
            hood = old.sub_grid((i, j), 3, 3, x_off=-1, y_off=-1)
            alive = sum(map(sum, hood.state)) - old[i][j]
            if old[i][j]:
                if alive < 2 or alive > 3:
                    # die
                    self.grid[i][j] = 0
            else:
                if alive == 3:
                    # revive
                    self.grid[i][j] = 1


class GOL2(gol_base):
    '''
    What if each cell stored it's life as an integer and on any step that it would survive it gets +1
    and on a step it dies it gets -1
    '''
    def __init__(self, columns: int, rows: int, initial_state:None|MGrid=None, w:float=0.5):
        self.columns = columns
        self.rows = rows
        if initial_state is None:
            life_choice = lambda: choice(range(1, 4)) if random() >= w else 0
            self.grid = MGrid(columns, rows, life_choice)
        else:
            self.grid = initial_state
            self.rows = len(initial_state)
            self.columns = len(initial_state[0])

    def next_frame(self):
        future = MGrid(self.columns, self.rows, lambda: 0)
        for i, j in product(range(self.columns), range(self.rows)):
            hood = self.grid.sub_grid((i, j), 3, 3, x_off=-1, y_off=-1)
            alive = hood.occupancy(skip=(1, 1))
            if self.grid[i][j] > 0:
                if alive < 2 or alive > 3:
                    # die
                    future[i][j] = max(0, self.grid[i][j] - 1)
                elif 2 <= alive <= 3:
                    future[i][j] = self.grid[i][j] + 1
            else:
                if alive == 3:
                    # revive
                    future[i][j] = 1
        return future

    def __next__(self):
        future = self.next_frame()
        if future.image() == self.grid.image():
            raise StopIteration()
        self.grid = future
        return future

