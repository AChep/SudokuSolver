# Copyright (C) 2015 Artem Chepurnoy <artemchep@gmail.com>
#
# This script is published under the terms of the MIT license.
# See http://opensource.org/licenses/mit-license.php

# Python 3 is required


from datetime import datetime

from sudoku import Sudoku


# Copyright Arto Inkala
# AI sudoku top 10 set 1
array = [
    # AI escargot
    """1 0 0 0 0 7 0 9 0
       0 3 0 0 2 0 0 0 8
       0 0 9 6 0 0 5 0 0
       0 0 5 3 0 0 9 0 0
       0 1 0 0 8 0 0 0 2
       6 0 0 0 0 4 0 0 0
       3 0 0 0 0 0 0 1 0
       0 4 0 0 0 0 0 0 7
       0 0 7 0 0 0 3 0 0""",
    # AI killer application
    """0 0 0 0 0 0 0 7 0
       0 6 0 0 1 0 0 0 4
       0 0 3 4 0 0 2 0 0
       8 0 0 0 0 3 0 5 0
       0 0 2 9 0 0 7 0 0
       0 4 0 0 8 0 0 0 9
       0 2 0 0 6 0 0 0 7
       0 0 0 1 0 0 9 0 0
       7 0 0 0 0 8 0 6 0""",
    # AI lucky diamond
    """1 0 0 5 0 0 4 0 0
       0 0 9 0 3 0 0 0 0
       0 7 0 0 0 8 0 0 5
       0 0 1 0 0 0 0 3 0
       8 0 0 6 0 0 5 0 0
       0 9 0 0 0 7 0 0 8
       0 0 4 0 2 0 0 1 0
       2 0 0 8 0 0 6 0 0
       0 0 0 0 0 1 0 0 2""",
    # AI worm hole
    """0 8 0 0 0 0 0 0 1
       0 0 7 0 0 4 0 2 0
       6 0 0 3 0 0 7 0 0
       0 0 2 0 0 9 0 0 0
       1 0 0 0 6 0 0 0 8
       0 3 0 4 0 0 0 0 0
       0 0 1 7 0 0 6 0 0
       0 9 0 0 0 8 0 0 5
       0 0 0 0 0 0 0 4 0""",
    # AI labyrinth
    """1 0 0 4 0 0 8 0 0
       0 4 0 0 3 0 0 0 9
       0 0 9 0 0 6 0 5 0
       0 5 0 3 0 0 0 0 0
       0 0 0 0 0 1 6 0 0
       0 0 0 0 7 0 0 0 2
       0 0 4 0 1 0 9 0 0
       7 0 0 8 0 0 0 0 4
       0 2 0 0 0 4 0 8 0""",
    # AI circles
    """0 0 5 0 0 9 7 0 0
       0 6 0 0 0 0 0 2 0
       1 0 0 8 0 0 0 0 6
       0 1 0 7 0 0 0 0 4
       0 0 7 0 6 0 0 3 0
       6 0 0 0 0 3 2 0 0
       0 0 0 0 0 6 0 4 0
       0 9 0 0 5 0 1 0 0
       8 0 0 1 0 0 0 0 2""",
    # AI squadron
    """6 0 0 0 0 0 2 0 0
       0 9 0 0 0 1 0 0 5
       0 0 8 0 3 0 0 4 0
       0 0 0 0 0 2 0 0 1
       5 0 0 6 0 0 9 0 0
       0 0 7 0 9 0 0 0 0
       0 7 0 0 0 3 0 0 2
       0 0 0 4 0 0 5 0 0
       0 0 6 0 7 0 0 8 0""",
    # AI honeypot
    """1 0 0 0 0 0 0 6 0
       0 0 0 1 0 0 0 0 3
       0 0 5 0 0 2 9 0 0
       0 0 9 0 0 1 0 0 0
       7 0 0 0 4 0 0 8 0
       0 3 0 5 0 0 0 0 2
       5 0 0 4 0 0 0 0 6
       0 0 8 0 6 0 0 7 0
       0 7 0 0 0 5 0 0 0""",
    # AI tweezers
    """0 0 0 0 1 0 0 0 4
       0 3 0 2 0 0 0 0 0
       6 0 0 0 0 8 0 9 0
       0 0 7 0 6 0 0 0 5
       9 0 0 0 0 5 0 8 0
       0 0 0 8 0 0 4 0 0
       0 4 0 9 0 0 1 0 0
       7 0 0 0 0 2 0 4 0
       0 0 5 0 3 0 0 0 7""",
    # AI broken brick
    """4 0 0 0 6 0 0 7 0
       0 0 0 0 0 0 6 0 0
       0 3 0 0 0 2 0 0 1
       7 0 0 0 0 8 5 0 0
       0 1 0 4 0 0 0 0 0
       0 2 0 9 5 0 0 0 0
       0 0 0 0 0 0 7 0 5
       0 0 9 1 0 0 0 3 0
       0 0 3 0 4 0 0 8 0""",
    # Empty test
    """0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0""",
]

n = 100
s = 0
for j in range(n):
    now = datetime.now()
    for i in array:
        sudoku = Sudoku(i)
        solved = sudoku.solve()
        if not solved:
            print("Failed to solve: \n%s" % i)
    delta = (datetime.now() - now).total_seconds()
    s += delta
print('Elapsed real time %fs.' % s)
print('Average real time %fs.' % (s / n))