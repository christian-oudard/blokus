from poly import Poly, gen_polys

max_size = 5
all_pieces = []
for size in range(1, max_size + 1):
    all_pieces.extend(gen_polys(size))
all_pieces.sort(key=lambda p: (len(p._points), p))

#for i, p in enumerate(all_pieces):
#    print()
#    print(i + 1)
#    print(p)

_empty = '.'
class Board:
    size = 14
    def __init__(self):
        self.data = {}

    def __str__(self):
        grid = [[_empty for _ in range(size)] for _ in range(size)]
        for point, color in self.data.items():
            x, y = point
            grid[y][x] = color
        return '\n'.join(''.join(line) for line in grid)

    def place_piece(self, piece, position, color):
        """
        Place a piece on the board.
        >>> Board.size = 5
        >>> board = Board()
        >>> a, b = sorted(all_pieces[17].orientations())[:2]
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
        """
        x, y = position
        for px, py in piece._points:
            self.data[(px + x, py + y)] = color
