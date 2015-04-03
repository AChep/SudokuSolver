# Copyright (C) 2015 Artem Chepurnoy <artemchep@gmail.com>
#
# This script is published under the terms of the MIT license.
# See http://opensource.org/licenses/mit-license.php

# Python 3 is required


class Clue:
    """
    A clue for solving the sudoku.

    Attributes:
        x              The X coordinate in a matrix of sudoku.
        y              The Y coordinate in a matrix of sudoku.
        possibilities  The list of possible values.
    """
    x = 0
    y = 0
    possibilities = []

    def __str__(self):
        return '(x=%d y=%d possibilities=%s)' % (self.x, self.y, self.possibilities)


class Sudoku:
    def __init__(self, sudoku="""8 0 0 0 0 0 0 0 0
                                 0 0 3 6 0 0 0 0 0
                                 0 7 0 0 9 0 2 0 0
                                 0 5 0 0 0 7 0 0 0
                                 0 0 0 0 4 5 7 0 0
                                 0 0 0 1 0 0 0 3 0
                                 0 0 1 0 0 0 0 6 8
                                 0 0 8 5 0 0 0 1 0
                                 0 9 0 0 0 0 4 0 0""", diagonal=False):
        sudoku = [[int(e) for e in row.split()] for row in sudoku.split('\n')]
        self._n = len(sudoku)
        for row in sudoku:
            if len(row) is not self._n:
                raise ValueError("The sudoku is missing some values.")
        # Basics.
        self._line = range(self._n)
        self._matrix = [[i // self._n, i % self._n] for i in range(self._n ** 2)]
        self._link_map = self._create_link_map(diagonal)

        '''
        Create the depth matrix & flat line. The depth variable is needed to
        simplify the best-position-search.
        '''
        self._depth_matrix = [[[float(len(self._link_map[i][j])), i, j] for j in self._line] for i in self._line]
        self._depth_line = []
        # Extract the matrix into a line.
        for e in self._depth_matrix:
            self._depth_line.extend(e)
        # Calculate the current depth state. Initially, the ceil with most links is
        # the best choice to set into.
        k = max(e[0] for e in self._depth_line) + 2
        for e in self._depth_line:
            e[0] = self._n - e[0] / k

        '''
        Create the possibilities matrix.
        '''
        # noinspection PyUnusedLocal
        self._x = [[list(range(-self._n, 0)) for j in self._line] for i in self._line]
        # Apply the initial values.
        for i, j in self._matrix:
            value = sudoku[i][j]
            if value:
                self.set(value, i, j)

    def _create_link_map(self, diagonal=False):
        n_region = int(self._n ** .5)
        # Check for the correct input.
        if n_region ** 2 != self._n:
            raise ValueError("Unsupported size of sudoku.")
        region = [[i // n_region, i % n_region] for i in self._line]
        # Create mapping.
        m = []
        for i in self._line:
            column = []
            for j in self._line:
                ceil = []
                # Add row.
                ceil.extend([[e, j] for e in self._line if e != i])
                # Add column.
                ceil.extend([[i, e] for e in self._line if e != j])
                # Add region.
                for a, b in region:
                    x = a + i // n_region * n_region
                    y = b + j // n_region * n_region
                    if x != i and y != j:
                        ceil.append([x, y])
                if diagonal:
                    # Add main diagonal.
                    if i == j:
                        ceil.extend([[e, e] for e in self._line if e != i])
                    # Add sub-diagonal.
                    if i == self._n - j - 1:
                        ceil.extend([[e, self._n - e - 1] for e in self._line if e != j])
                column.append(ceil)
            m.append(column)
        return m

    def set(self, value, x, y):
        """

        :param value: Value to be set
        :param x: X coordinate
        :param y: Y coordinate
        """
        if 0 < value <= self._n and -value in self._x[x][y]:
            self._set(-value, x, y)
            self._depth_line.remove(self._depth_matrix[x][y])
        else:
            raise ValueError('Failed to set %d to [%d;%d]!' % (value, y + 1, x + 1))
        # Re-sort the depth map.
        self._depth_line.sort(key=lambda e: e[0])

    def clue(self):
        """
        :return:
        The best possible step.
        """
        clue = Clue()
        clue.x = self._depth_line[0][1]
        clue.y = self._depth_line[0][2]
        clue.possibilities = [-e for e in self._x[clue.x][clue.y]]
        return clue

    def solve(self):
        """

        :return:
        <i>True</i> if one or more solutions of this sudoku exists,
        <i>False</i> otherwise.
        """
        solution = self._solve()
        self._x = solution
        return bool(solution)

    def _solve(self):
        if not len(self._depth_line):
            # Found the solution!
            return self._x
        clue = self._depth_line[0]
        if clue[0] <= 0:
            # Found an empty ceil with no
            # possible values.
            return None
        i, j = clue[1], clue[2]
        # Remove this ceil.
        del self._depth_line[0]
        # Try all possibilities.
        x_value = self._x[i][j]
        for value in x_value:
            log = []
            self._set(value, i, j, log)
            self._depth_line.sort(key=lambda e: e[0])

            # Try to solve it.
            if not self._solve() is None:
                return self._x

            # Restore everything.
            self._x[i][j] = x_value
            for k in log:
                a, b = k >> 16, k & (1 << 16) - 1
                self._x[a][b].append(value)
                self._depth_matrix[a][b][0] += 1
            self._depth_line.sort(key=lambda e: e[0])
        # Put the ceil back.
        self._depth_line.insert(0, clue)
        return None

    def _set(self, value, i, j, fallback=None):
        self._x[i][j] = [-value]

        # Remove this element from
        # other linked cells.
        for a, b in self._link_map[i][j]:
            try:
                self._x[a][b].remove(value)
                self._depth_matrix[a][b][0] -= 1
                # Remember the ceil's location
                if fallback is not None:
                    fallback.append(a << 16 | b)
            except ValueError:
                pass

    @property
    def solution(self):
        return self._x

    @staticmethod
    def format(x):
        return '\n'.join([' '.join([str(e[0]) for e in row]) for row in x])