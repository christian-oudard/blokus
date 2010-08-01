"""
Place pieces on the board.
>>> from blokus import Board
>>> Board.size = 5
>>> board = Board()
>>> from pieces import five_f
>>> a, b = sorted(five_f.orientations())[:2]
>>> print(a)
#
###
 #
>>> print(b)
##
 ##
 #
>>> board.place_piece(a, (0, 0), 'X')
>>> print(board)
X....
XXX..
.X...
.....
.....
>>> board.place_piece(b, (2, 2), 'O')
>>> print(board)
X....
XXX..
.XOO.
...OO
...O.

>>> from pieces import four_o

Cannot place a piece off the board.
>>> Board.size = 3
>>> board = Board()
>>> board.place_piece(four_o, (-1, -1), 'X')
Traceback (most recent call last):
    ...
ValueError: Piece out of bounds
>>> board.place_piece(four_o, (2, 2), 'X')
Traceback (most recent call last):
    ...
ValueError: Piece out of bounds

Cannot place a piece on top of another piece.
>>> Board.size = 3
>>> board = Board()
>>> board.place_piece(four_o, (0, 0), 'X')
>>> print(board)
XX.
XX.
...
>>> board.place_piece(four_o, (1, 0), 'O')
Traceback (most recent call last):
    ...
ValueError: Overlapping pieces
>>> print(board)
XX.
XX.
...

Cannot place a piece next to another piece of your color.
STUB

Your pieces must connect at the corners.
STUB
"""
