""" Main file for the solver """

# Copyright (C) 2015 Artem Chepurnoy <artemchep@gmail.com>
#
# This script is published under the terms of the MIT license.
# See http://opensource.org/licenses/mit-license.php

# Python 3 is required


from sudoku import Sudoku

S = Sudoku()
print(S.clue())
print(S.solve())
print(Sudoku.format(S.solution))
