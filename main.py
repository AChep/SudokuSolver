from sudoku import Sudoku

s = Sudoku()
print(s.clue())
print(s.solve())
print(Sudoku.format(s.solution))