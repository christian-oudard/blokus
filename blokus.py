_empty = '.'
class Board:
    size = 14
    def __init__(self):
        self.data = {}

    def __str__(self):
        grid = [[_empty for _ in range(self.size)] for _ in range(self.size)]
        for point, color in self.data.items():
            x, y = point
            grid[y][x] = color
        return '\n'.join(''.join(line) for line in grid)

    def place_piece(self, piece, position, color):
        """
        Place a piece on the board.
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

        Cannot place a piece on top of another piece.
        >>> Board.size = 3
        >>> board = Board()
        >>> from pieces import four_o
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
        x, y = position
        for px, py in piece._points:
            point = px + x, py + y
            if point in self.data:
                raise ValueError('Overlapping pieces')
            self.data[point] = color
