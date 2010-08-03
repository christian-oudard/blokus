from collections import defaultdict

class Board:
    _empty = '.'
    _start = '_'
    size = 14
    start_points = (
        (4, 4),
        (9, 9),
    )
    def __init__(self):
        self.data = {}

    def __str__(self):
        grid = [[self._empty for _ in range(self.size)] for _ in range(self.size)]
        for x, y in self.start_points:
            try:
                grid[y][x] = self._start
            except IndexError:
                pass
        for point, color in self.data.items():
            x, y = point
            try:
                grid[y][x] = color
            except IndexError:
                pass
        return '\n'.join(''.join(line) for line in grid)

    def is_first(self, color):
        return not any(v == color for v in self.data.values())

    def place_piece(self, piece, color):
        reason = self._check_place_piece(piece, color)
        if reason:
            raise ValueError(reason)
        self._place_piece(piece, color)

    def _place_piece(self, piece, color):
        for point in piece:
            self.data[point] = color

    def _check_place_piece(self, piece, color):
        # Check bounds.
        for point in piece:
            if not self.in_bounds(point):
                return 'Piece out of bounds'
        # Check overlaps
        for point in piece:
            if point in self.data.keys():
                return 'Overlapping pieces'
        # Check adjacencies.
        for adj in piece.adjacencies():
            if self.data.get(adj) == color:
                return 'Cannot play next to a piece of the same color'

        if self.is_first(color):
            # Check start points.
            if not any(p in self.start_points for p in piece):
                return 'Must play on a start point'
        else:
            # Check corner connections.
            if not any(
                self.data.get(corner) == color
                for corner in piece.corner_adjacencies()
            ):
                return 'Must play with corners touching a piece of the same color'

        return None # No problems

    def legal_moves(self, player, pieces):
        for c_piece in pieces:
            for piece in c_piece.orientations():
                for x in range(self.size):
                    for y in range(self.size):
                        location = x, y
                        t_piece = piece.translated(location)
                        reason = self._check_place_piece(piece, player)
                        if reason is None:
                            yield piece, location

    def in_bounds(self, point):
        x, y = point
        return (x >= 0 and y >= 0 and
                x < self.size and y < self.size)
