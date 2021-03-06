SudokuSolver
============
[![Code Climate](https://codeclimate.com/github/AChep/SudokuSolver/badges/gpa.svg)](https://codeclimate.com/github/AChep/SudokuSolver) [![Support at gratipay](http://img.shields.io/gratipay/AChep.svg)](https://gratipay.com/AChep/)

<img alt="Default sudoku" align="right" height="300"
   src="https://github.com/AChep/SudokuSolver/raw/master/art/sudoku.jpg" />

This Sudoku solver has been written just for fun by a Python noob. It can solve the hardest Sudokus in less than half a second (for example, it solves the _AI top 10_ in _1.3s_.)

**PS**: The puzzle may be 2x2, 4x4, 9x9, 16x16, 25x25, ..., _n^2xn^2_

<a href="bitcoin:1GYj49ZnMByKj2f6p7r4f92GQi5pR6BSMz?amount=0.005">
  <img alt="Bitcoin wallet: 1GYj49ZnMByKj2f6p7r4f92GQi5pR6BSMz" vspace="28" hspace="20"
       src="https://github.com/AChep/SudokuSolver/raw/master/art/btn_bitcoin.png" />
</a> <a href="http://goo.gl/UrecGo">
  <img alt="PayPal" vspace="28"
       src="https://github.com/AChep/SudokuSolver/raw/master/art/btn_paypal.png" />
</a>

Report a bug or request a feature
----------------
Before creating a new issue please make sure that same or similar issue is not already created by checking [open issues][2] and [closed issues][3] *(please note that there might be multiple pages)*. If your issue is already there, don't create a new one, but leave a comment under already existing one.

Checklist for creating issues:

- Keep titles short but descriptive.
- For feature requests leave a clear description about the feature with examples where appropriate.
- For bug reports leave as much information as possible about your device, android version, etc.
- For bug reports also write steps to reproduce the issue.

[Create new issue][1]

How to solve a Sudoku?
----------------
To enter the Sudoku from a console:

``` bash
$ python sudoku.py
# It will ask you to enter the Sudoku.
```

To load the Sudoku from a file:

``` bash
$ python sudoku.py filename.txt
# An example of a file:
# filename.txt
# 8 0 0 0 0 0 0 0 0
# 0 0 3 6 0 0 0 0 0
# 0 7 0 0 9 0 2 0 0
# 0 5 0 0 0 7 0 0 0
# 0 0 0 0 4 5 7 0 0
# 0 0 0 1 0 0 0 3 0
# 0 0 1 0 0 0 0 6 8
# 0 0 8 5 0 0 0 1 0
# 0 9 0 0 0 0 4 0 0
```

[1]: https://github.com/AChep/SudokuSolver/issues/new
[2]: https://github.com/AChep/SudokuSolver/issues?state=open
[3]: https://github.com/AChep/SudokuSolver/issues?state=closed
