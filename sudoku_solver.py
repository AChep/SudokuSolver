# Copyright (C) 2015 Artem Chepurnoy <artemchep@gmail.com>
#
# This script is published under the terms of the MIT license.
# See http://opensource.org/licenses/mit-license.php

# Python 3 is required

import sys

from datetime import datetime
from functools import reduce

def create_link_map(n):
    region_n = int(n**(.5))
    region_range = [[i // region_n, i % region_n] for i in range(n)]
    # Create initial map of links, so
    # we may multiply use those.
    w = [[[i, j] for j in range_9] for i in range_9]
    m = []
    for i in range_9:
        column = []
        for j in range_9:
            ceil = []
            # Add row.
            ceil.extend([w[e][j] for e in range_9 if e != i])
            # Add column.
            ceil.extend([w[i][e] for e in range_9 if e != j])
            # Add region.
            for a, b in region_range:
                x = a + i // region_n * region_n;
                y = b + j // region_n * region_n;
                if x != i and y != j:
                    ceil.append(w[x][y])
            '''
            # Add main diagonal.
            if i == j:
                ceil.extend([w[e][e] for e in range_9 if e != i])
            # Add sub-diagonal.
            if i == n - j - 1:
                ceil.extend([w[e][n - e - 1] for e in range_9 if e != j])
            '''
            column.append(ceil)
        m.append(column)
    return m

def set_value(x, value, i, j):
    x[i][j] = temp_values_list[-value - 1]
    z.remove(z_map[i][j])

    # Remove this element from 
    # other linked ceils.
    for a, b in link_map[i][j]:
        try:
            x[a][b].remove(value)
            z_map[a][b][0] -= 1
        except ValueError:
            pass

def restore(x, log):
    for e, value, i, j, l in log:
        x[i][j] = e
        for a in l:
            x[a >> 16][a & (1 << 16) - 1].append(value)
 
def solve(x):
    global iterations
    iterations += 1
    if not iterations % 10000:
        print('%d...' % iterations)
    if not len(z):
        # Found the solution!
        return x
    z_item = z[0]
    if  z_item[0] <= 0:
        # Found an empty ceil with no
        # possible values.
        return None
    i, j = z_item[1], z_item[2]
    # Remove this ceil.
    del z[0]
    # Try all possibilities.
    x_value = x[i][j]
    for value in x_value:
        x[i][j] = temp_values_list[-value - 1]

        # Remove this element from 
        # other linked ceils.
        log = []
        for a, b in link_map[i][j]:
            try:
                x[a][b].remove(value)
                log.append(a << 16 | b) # Remember the ceil's location
                z_map[a][b][0] -= 1
            except ValueError:
                pass
        z.sort(key=lambda e : e[0])

        # Try to solve it.
        if not solve(x) is None:
            return x

        # Restore everything.
        x[i][j] = x_value
        for k in log:
            a, b = k >> 16, k & (1 << 16) - 1
            x[a][b].append(value)
            z_map[a][b][0] += 1
        z.sort(key=lambda e : e[0])
    # Put the ceil back.
    z.insert(0, z_item)
    return None

'''
Enter data.
'''
# '0' means an unknown value.
sudoku = """8 0 0 0 0 0 0 0 0
            0 0 3 6 0 0 0 0 0
            0 7 0 0 9 0 2 0 0
            0 5 0 0 0 7 0 0 0
            0 0 0 0 4 5 7 0 0
            0 0 0 1 0 0 0 3 0
            0 0 1 0 0 0 0 6 8
            0 0 8 5 0 0 0 1 0
            0 9 0 0 0 0 4 0 0"""

# Prepare the naked data of sudoku.
sudoku = [[int(e) for e in row.split()] for row in sudoku.split('\n')]
sudoku_length = len(sudoku)

# Change the maximum recursion depth, so
# this puzzle can be solved.
sys.setrecursionlimit(max(sudoku_length**2 + 10, 25))

range_9 = range(sudoku_length)
range_99 = [[i // sudoku_length, i % sudoku_length] for i in range(sudoku_length ** 2)]
temp_values_list = [[e + 1] for e in range_9]

'''
Solve the sudoku!
'''
now = datetime.now()
iterations = 0

# Link everything
link_map = create_link_map(sudoku_length)

z_map = [[[float(len(link_map[i][j])), i, j] for j in range_9] for i in range_9]
z = []
for e in z_map:
    z.extend(e)
k = max(e[0] for e in z) + 2
for e in z:
     e[0] = sudoku_length - e[0] / k
z.sort(key=lambda e : e[0])

# Create the list of posibilities.
x = [[list(range(-sudoku_length, 0)) for j in range_9] for i in range_9]
# Apply the initial sudoku.
for i, j in range_99:
    value = sudoku[i][j]
    #print(e)
    if value:
        if -value in x[i][j]:
            set_value(x, -value, i, j)
        else:
            print('The sudoku is incorrect!')
            print('Could not place %d in [%d;%d]!' % (value, j + 1, i + 1))
            sys.exit()
sudoku = None
# Solve
x = solve(x)

'''
Write the solution to user.
'''
elapsed_time = (datetime.now() - now).total_seconds()
if not x is None:
    print('The solution is:')
    print('\n'.join([' '.join([str(e[0]) for e in r]) for r in x]))
else:
    print('No solution!')
print(' '.join(['-' for i in range_9]))
print('Solved in %fs.' % elapsed_time)
print('Iterations: %d' % iterations)
