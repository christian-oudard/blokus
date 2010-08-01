"""
>>> from board import Board
>>> from pieces import two_i, four_o, five_f

For testing purposes, count everything as a start point.
Three or more dots has special meaning to doctest, use comma for empty squares
>>> Board.start_points = tuple((x, y) for x in range(20) for y in range(20))
>>> Board._empty = ','
>>> Board._start = ','



Place pieces on the board.
>>> Board.size = 5
>>> board = Board()
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
X,,,,
XXX,,
,X,,,
,,,,,
,,,,,
>>> board.place_piece(b, (2, 2), 'O')
>>> print(board)
X,,,,
XXX,,
,XOO,
,,,OO
,,,O,


Cannot place a piece off the board.
>>> Board.size = 3
>>> board = Board()
>>> board.place_piece(four_o, (-1, -1), 'X')
Traceback (most recent call last):
    ...
ValueError: Piece out of bounds
>>> print(board)
,,,
,,,
,,,
>>> board.place_piece(four_o, (2, 2), 'X')
Traceback (most recent call last):
    ...
ValueError: Piece out of bounds
>>> print(board)
,,,
,,,
,,,

Cannot place a piece on top of another piece.
>>> Board.size = 3
>>> board = Board()
>>> board.place_piece(four_o, (0, 0), 'X')
>>> print(board)
XX,
XX,
,,,
>>> board.place_piece(four_o, (1, 0), 'O')
Traceback (most recent call last):
    ...
ValueError: Overlapping pieces
>>> print(board)
XX,
XX,
,,,

Cannot place a piece next to another piece of your color.
>>> Board.size = 3
>>> board = Board()
>>> board.place_piece(two_i, (0, 0), 'X')
>>> print(board)
X,,
X,,
,,,
>>> board.place_piece(two_i, (1, 1), 'X')
Traceback (most recent call last):
    ...
ValueError: Cannot play next to a piece of the same color
>>> print(board)
X,,
X,,
,,,

Your pieces must connect at the corners.
>>> Board.size = 4
>>> board = Board()
>>> board.place_piece(two_i, (0, 0), 'X')
>>> print(board)
X,,,
X,,,
,,,,
,,,,
>>> board.place_piece(four_o, (2, 0), 'X')
Traceback (most recent call last):
    ...
ValueError: Must play with corners touching a piece of the same color
>>> print(board)
X,,,
X,,,
,,,,
,,,,
>>> board.place_piece(four_o, (1, 2), 'X')
>>> print(board)
X,,,
X,,,
,XX,
,XX,

You must start on a designated start point.
>>> Board.size = 4
>>> Board.start_points = ((0, 0), (3, 3))
>>> Board._start = 'o'
>>> board = Board()
>>> print(board)
o,,,
,,,,
,,,,
,,,o
>>> board.place_piece(four_o, (0, 2), 'X')
Traceback (most recent call last):
    ...
ValueError: Must play on a start point
>>> print(board)
o,,,
,,,,
,,,,
,,,o
>>> board.place_piece(four_o, (2, 2), 'X')
>>> print(board)
o,,,
,,,,
,,XX
,,XX
"""
