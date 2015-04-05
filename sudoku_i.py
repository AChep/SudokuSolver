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


# TODO: Locked candidate.
class _Group:
    def __init__(self, cells, data):
        self.data = data
        self.cells = cells
        # Link this group to the cells.
        for ceil in cells:
            ceil.groups.append(self)
        # Create depth map.
        self.depth = [1] * data.size
        # Create pairs dict.
        self.pairs = {}

    def on_ceil_value_set_pre(self, ceil, value):
        # Remove the ceil from list.
        self.cells.remove(ceil)

        # Hidden loners.
        self.depth[value - 1] = -self.data.size
        for i in ceil.ghost:
            self.depth[-i - 1] += 1

    def on_ceil_value_set(self, ceil, value):
        # Open loners.
        for i in self.cells:
            i.abandon(-value)

    def on_ceil_value_abandoned_pre(self, ceil, value):
        key = frozenset(ceil.value)
        try:
            self.pairs[key] -= 1
        except KeyError:
            self.pairs[key] = self.data.size - 1

    def on_ceil_value_abandoned(self, ceil, value):
        # Hidden loners.
        self.depth[-value - 1] += 1

        # Open pairs
        has_open_pairs = False
        key = frozenset(ceil.value)
        try:
            self.pairs[key] += 1
            if self.pairs[key] == len(ceil.value) > 1:
                has_open_pairs = True
        except KeyError:
            self.pairs[key] = 1

        # Locked candidate.
        lc = []
        possibly_has_locked_candidates = self.data.size > self.depth[-value - 1] > 0

        for i in self.cells:
            if i is ceil:
                continue
            # Hidden loners.
            if self.depth[-value - 1] == self.data.size and value in i.value:
                # Simplify the superposition.
                for k in i.value:
                    if k != value:
                        i.abandon(k)
            # Open pairs.
            if has_open_pairs and ceil.value in i.value:
                # Simplify the superposition.
                for k in ceil.value:
                    if k not in i.value:
                        i.abandon(k)
            # Locked candidate.
            if possibly_has_locked_candidates and value in i.value:
                lc.append(i)
            continue

        # Locked candidate.
        if lc:
            groups = list(lc[0].groups)
            groups.remove(self)
            for i in lc:
                groups[:] = [j for j in groups if j in i.groups]
                if not groups:
                    break
            else:
                for i in groups:
                    for j in i.cells:
                        if j not in lc:
                            j.abandon(value)


class Sudoku:
    def __init__(self, sudoku):
        # Parse the source of a sudoku.
        sudoku = [[int(e) for e in row.split()] for row in sudoku.split('\n')]

        self._data = _Data()
        self._data.i = 0
        self._data.log = []
        self._data.size = len(sudoku)
        line = list(range(self._data.size))
        region_size = int(self._data.size ** .5)
        region = [[i // region_size, i % region_size] for i in line]

        # Create the cells.
        # noinspection PyUnusedLocal
        self._cells = [[_Ceil(self._data) for j in line] for i in line]
        self._cells_line = list(itertools.chain.from_iterable(self._cells))

        # Create the groups.
        for j in line:
            # Add a row.
            _Group([self._cells[e][j] for e in line], self._data)
            # Add a column.
            _Group([self._cells[j][e] for e in line], self._data)
        # Add regions.
        for i, j in region:
            r = []
            for a, b in region:
                x = a + i * region_size
                y = b + j * region_size
                r.append([x, y])
            _Group([self._cells[e[0]][e[1]] for e in r], self._data)

        # Apply the initial values.
        for i in line:
            for j in line:
                v = sudoku[i][j]
                if v:
                    self._cells[i][j].set(v)
                    self._cells_line.remove(self._cells[i][j])

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
                # possible values.
                return False
            del self._cells_line[0]

            value = ceil.value[0]
            ceil.set(-value)
            self._cells_line.sort(key=lambda e: len(e.value))
        return True

    @property
    def solution(self):
        return [[i.value for i in row] for row in self._cells]
