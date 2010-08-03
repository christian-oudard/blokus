"""
>>> from board import Board
>>> from pieces import all_pieces, two, four_o, five_f, five_z, four_s, five_w, five_v

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
>>> board.place_piece(a.translated(0, 0), 'X')
>>> print(board)
X,,,,
XXX,,
,X,,,
,,,,,
,,,,,
>>> board.place_piece(b.translated(2, 2), 'O')
>>> print(board)
X,,,,
XXX,,
,XOO,
,,,OO
,,,O,


Cannot place a piece off the board.
>>> Board.size = 3
>>> board = Board()
>>> board.place_piece(four_o.translated(-1, -1), 'X', reason=True)
Traceback (most recent call last):
    ...
ValueError: Piece out of bounds
>>> print(board)
,,,
,,,
,,,
>>> board.place_piece(four_o.translated(2, 2), 'X', reason=True)
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
>>> board.place_piece(four_o.translated(0, 0), 'X', reason=True)
>>> print(board)
XX,
XX,
,,,
>>> board.place_piece(four_o.translated(1, 0), 'O', reason=True)
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
>>> board.place_piece(two.translated(0, 0), 'X')
>>> print(board)
X,,
X,,
,,,
>>> board.place_piece(two.translated(1, 1), 'X', reason=True)
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
>>> board.place_piece(two.translated(0, 0), 'X')
>>> print(board)
X,,,
X,,,
,,,,
,,,,
>>> board.place_piece(four_o.translated(2, 0), 'X', reason=True)
Traceback (most recent call last):
    ...
ValueError: Must play with corners touching a piece of the same color
>>> print(board)
X,,,
X,,,
,,,,
,,,,
>>> board.place_piece(four_o.translated(1, 2), 'X')
>>> print(board)
X,,,
X,,,
,XX,
,XX,

You must start on a designated start point.
>>> Board.size = 4
>>> Board.start_points = ((0, 0), (3, 3))
>>> Board._start = '_'
>>> board = Board()
>>> print(board)
_,,,
,,,,
,,,,
,,,_
>>> board.place_piece(four_o.translated(0, 2), 'X', reason=True)
Traceback (most recent call last):
    ...
ValueError: Must play on a start point
>>> print(board)
_,,,
,,,,
,,,,
,,,_
>>> board.place_piece(four_o.translated(2, 2), 'X')
>>> print(board)
_,,,
,,,,
,,XX
,,XX

Test finding all moves.
>>> Board.size = 14
>>> Board.start_points = ((4, 4), (9, 9))

>>> board = Board()
>>> list(board.legal_moves('X', []))
[]

>>> moves = list(board.legal_moves('X', all_pieces))
>>> len(moves)
828

>>> a = sorted(four_s.orientations())[1]
>>> board.place_piece(a.translated(8, 9), 'X')
>>> b = sorted(five_z.orientations())[3]
>>> board.place_piece(b.translated(11, 7), 'X')
>>> c = sorted(five_w.orientations())[2]
>>> board.place_piece(c.translated(6, 7), 'X')
>>> d = sorted(five_v.orientations())[1]
>>> board.place_piece(d.translated(3, 8), 'X')
>>> print(board)
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,_,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,XX,,,XX
,,,X,,XX,,,,X,
,,,X,,X,XX,XX,
,,,XXX,,,XX,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
>>> pieces = [p for p in all_pieces if p not in (a, b, c, d)]
>>> moves = list(board.legal_moves('X', pieces))
>>> len(moves)
854


Play a game between bots.
>>> from play import play_game
>>> import bot_null
>>> play_game(bot_null, bot_null)
(89, 89)
>>> import bot_simple
>>> a, b = play_game(bot_simple, bot_simple)
>>> assert a < 89
>>> assert b < 89
"""
