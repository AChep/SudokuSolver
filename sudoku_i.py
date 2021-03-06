# Copyright (C) 2015 Artem Chepurnoy <artemchep@gmail.com>
#
# This script is published under the terms of the MIT license.
# See http://opensource.org/licenses/mit-license.php

# Python 3 is required

import itertools

from sudoku import Clue


class _Data:
    pass


class _Ceil:
    def __init__(self, data):
        self.data = data
        self.ghost = self.value = [-i - 1 for i in range(data.size)]
        self.groups = []

    def __repr__(self):
        return "<Ceil value:%s>" % self.value

    def set(self, value):
        self.ghost = self.value
        self.value = [value]
        # Notify the groups.
        for i in self.groups:
            i.on_ceil_value_set_pre(self, value)
        # Notify the groups.
        for i in self.groups:
            i.on_ceil_value_set(self, value)
        # Clean-up the ghost.
        self.ghost = None

    def abandon(self, value):
        for i, j in enumerate(self.value):
            if j == value:
                # Notify the groups.
                for k in self.groups:
                    k.on_ceil_value_abandoned_pre(self, value)
                del self.value[i]
                break
        else:
            return False
        # Notify the groups.
        for i in self.groups:
            i.on_ceil_value_abandoned(self, value)
        return True

    def issubset(self, ceil):
        """
        Report whether another super-position contains this super-position.
        """
        if ceil is self:
            return True
        for v in ceil.value:
            if v not in self.value:
                return False
        return True


class _Group:
    def __init__(self, cells, data):
        self.data = data
        self.cells = cells
        self.queue = []
        # Link this group to the cells.
        for ceil in cells:
            ceil.groups.append(self)
        # Create depth map.
        self.depth = [1] * data.size

    def on_ceil_value_set_pre(self, ceil, value):
        # Remove the ceil from list.
        self.cells.remove(ceil)

        # Hidden singles
        self.depth[value - 1] = -self.data.size
        for i in ceil.ghost:
            self.depth[-i - 1] += 1

    def on_ceil_value_set(self, ceil, value):
        # Naked singles
        for i in self.cells:
            i.abandon(-value)

    def on_ceil_value_abandoned_pre(self, ceil, value):
        self.depth[-value - 1] += 1

    def on_ceil_value_abandoned(self, ceil, value):
        self._method_hidden_singles(ceil, value)
        self._method_hidden_candidates(ceil, value)
        self._method_naked_candidates(ceil, value)
        self._method_intersection_removal(ceil, value)
        # Handle queue.
        for ceil, value in self.queue:
            ceil.abandon(value)
        self.queue.clear()

    def _method_hidden_singles(self, ceil, value):
        """
        Hidden Single means that for a given digit and house only one cell
        is left to place that digit. The cell itself has more than one candidate
        left, the correct digit is thus hidden amongst the rest.

        This is the same as the Pointing Singles.
        """
        if self.depth[-value - 1] == self.data.size:
            for i in self.cells:
                if i is not ceil and value in i.value:
                    # Simplify the superposition.
                    for k in i.value:
                        if k != value:
                            self._post_abandon(i, k)
                    break

    def _method_hidden_candidates(self, ceil, value):
        """
        Read more: http://www.sudokuwiki.org/Hidden_Candidates
        """
        cells = []
        for n in range(2, int(self.data.size ** 0.5) * 2):
            # Get
            base_elements = [-i - 1 for i, depth in enumerate(self.depth) if depth == self.data.size - n + 1]
            for v in base_elements:
                merge = [0] * self.data.size
                for ceil in self.cells:
                    if v in ceil.value:
                        cells.append(ceil)
                        for k in ceil.value:
                            merge[-k - 1] += 1
                        if len(cells) == n:
                            break
                size = 0
                for i, m in enumerate(merge):
                    if m != 0 and self.depth[i] >= self.data.size - n + 1:
                        size += 1
                        merge[i] = 0
                        if self.depth[i] != self.data.size - m + 1:
                            break
                else:
                    if size == n:
                        for i, k in enumerate(merge):
                            if k != 0:
                                for ceil in cells:
                                    self._post_abandon(ceil, -i - 1)
                cells.clear()

    def _method_naked_candidates(self, ceil, value):
        """
        Naked Pair.
        A Naked Pair (also known as a Conjugate Pair) is a set of two candidate
        numbers sited in two cells that belong to at least one unit in common.
        That is they reside in the same row, box or column.

        Naked Triples
        A Naked Triple is slightly more complicated because it does not always
        imply three numbers each in three cells.
        Any group of three cells in the same unit that contain IN TOTAL three
        candidates is a Naked Triple. Each cell can have two or three numbers,
        as long as in combination all three cells have only three numbers.
        When this happens, the three candidates can be removed from all other
        cells in the same unit.

        Naked Quads
        A Naked Quad is rarer, especially in its full form but still useful if they
        can be spotted. The same logic from Naked Triples applies, but the reason
        it is so rare is because if a Quad is present the remaining cells are
        more like to be a Triple or Pair and the solver will highlight those first.

        Read more: http://www.sudokuwiki.org/Naked_Candidates
        """
        if len(ceil.value) == self.data.size - 1:
            # 1. The length can't be equal to the size.
            # 2. If the length is equal to a `size - 1`
            # then it's up to a Naked Singles method to
            # handle it
            return
        s = []
        cells = []
        # Find all the cells that are depending on the
        # changed one.
        for i in self.cells:
            if i is not ceil and len(i.value) < self.data.size - 1:  # Ignore Naked Singles
                if ceil.issubset(i):
                    cells.append(i)  # Have to re-check this one.
        for i in cells:
            for j in self.cells:
                if i.issubset(j):
                    s.append(j)
            length = len(s)
            if length == len(i.value):
                for v in i.value:
                    size = self.data.size - self.depth[-v - 1] + 1
                    if size == length:
                        # This value exists only in our naked candidates,
                        # so there's no need to try to remove it from others.
                        continue
                    # Remove the value from an un-linked cells.
                    p = 0
                    for j in self.cells:
                        if p == length or j is not s[p]:
                            size -= 1
                            self._post_abandon(j, v)
                            if not size:
                                # No cells left in which it's possible to
                                # abandon the value.
                                break
                        else:
                            p += 1
            s.clear()
        del s, cells

    def _method_intersection_removal(self, ceil, value):
        size = self.data.size
        if size > self.depth[-value - 1] > size - size ** 0.5:
            cells = groups = None
            for i in self.cells:
                if i is not ceil and value in i.value:
                    if cells is None:
                        cells = []
                        groups = list(i.groups)
                        groups.remove(self)
                    else:
                        groups = [j for j in groups if j in i.groups]
                        if not groups:  # True if not empty
                            return None
                    cells.append(i)
            if groups:
                for i in groups:
                    for j in i.cells:
                        if j not in cells:
                            self._post_abandon(j, value)

    def _post_abandon(self, ceil, value):
        self.queue.append([ceil, value])


class Sudoku:
    def __init__(self, sudoku):
        # Parse the source of a sudoku.
        sudoku = [[int(e) for e in row.split()] for row in sudoku.split('\n')]

        self._data = _Data()
        self._data.i = 0
        self._data.log = []
        self._data.size = len(sudoku)
        line = list(range(self._data.size))

        # Create the cells.
        # noinspection PyUnusedLocal
        self._cells = [[_Ceil(self._data) for j in line] for i in line]
        self._cells_line = list(itertools.chain.from_iterable(self._cells))

        # Init other parts.
        self._init_groups()
        self._init_sudoku(sudoku)

    def _init_groups(self):
        """
        Links all cells to groups. Group is a consists of the cells which
        must have unique values. This method defines the default rules of
        the Sudoku game.
        """
        line = range(self._data.size)
        # Create the groups.
        for j in line:
            # Add a row. Creating group automatically links the
            # cells, so no additional moves needed.
            _Group([self._cells[e][j] for e in line], self._data)
            # Add a column.
            _Group([self._cells[j][e] for e in line], self._data)
        # Add regions.
        region_size = int(self._data.size ** .5)
        region = [[i // region_size, i % region_size] for i in line]
        for i, j in region:
            r = []
            for a, b in region:
                x = a + i * region_size
                y = b + j * region_size
                r.append([x, y])
            _Group([self._cells[x][y] for x, y in r], self._data)

    def _init_sudoku(self, sudoku):
        """
        Loads the initial state of the sudoku from the int matrix,
        passed as an argument. This should not be called manually.
        :param sudoku:
        The int matrix that defines the Sudoku. Zero means 'unknown value'.
        :raises Exception:
        """
        line = range(self._data.size)
        # Apply the initial values.
        for i in line:
            for j in line:
                v = sudoku[i][j]
                if v:
                    ceil = self._cells[i][j]
                    # Check for correct data.
                    if -v not in ceil.value:
                        raise Exception
                    # Set the value
                    ceil.set(v)
                    self._cells_line.remove(ceil)

        # Sort the best positions.
        self._cells_line.sort(key=lambda e: len(e.value))

    def clue(self):
        if not self._cells_line:
            return None  # The sudoku is solved.
        ceil = self._cells_line[0]
        # noinspection PyUnresolvedReferences
        line = list(range(self._data.size))
        try:
            for a in line:
                for b in line:
                    if self._cells[a][b] is ceil:
                        i, j = a, b
                        # Break both loops.
                        raise LookupError()
            else:
                # This should never happen.
                raise ValueError
        except LookupError:
            pass

        clue = Clue()
        # noinspection PyUnboundLocalVariable
        clue.x = i
        # noinspection PyUnboundLocalVariable
        clue.y = j
        clue.possibilities = [-e for e in ceil.value]
        return clue

    def solve(self, guess=False):
        while self._cells_line:
            # Choose the best candidate.
            ceil = self._cells_line[0]
            size = len(ceil.value)
            if not size or not guess and size != 1:
                # Found an empty ceil with no
                # possible values or the ceil
                # with multiple possible values.
                return False
            del self._cells_line[0]

            value = ceil.value[0]
            ceil.set(-value)
            self._cells_line.sort(key=lambda e: len(e.value))
        return True

    @property
    def solution(self):
        return [[i.value for i in row] for row in self._cells]
