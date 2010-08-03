from collections import defaultdict
from poly import translate, adjacencies, corner_adjacencies

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

    def place_piece(self, piece, position, color):
        reason = self._check_place_piece(piece, position, color)
        if reason:
            raise ValueError(reason)
        self._place_piece(piece, position, color)

    def _place_piece(self, piece, position, color):
        piece = piece.translated(*position)
        for point in piece._points:
            self.data[point] = color

    def _check_place_piece(self, piece, position, color):
        points = list(translate(piece._points, *position))
        # Check bounds.
        for point in points:
            if not self.in_bounds(point):
                return 'Piece out of bounds'
        # Check overlaps
        for point in points:
            if point in self.data.keys():
                return 'Overlapping pieces'
        # Check adjacencies.
        for adj in adjacencies(points):
            if self.data.get(adj) == color:
                return 'Cannot play next to a piece of the same color'

        if self.is_first(color):
            # Check start points.
            if not any(p in self.start_points for p in points):
                return 'Must play on a start point'
        else:
            # Check corner connections.
            if not any(
                self.data.get(corner) == color
                for corner in corner_adjacencies(points)
            ):
                return 'Must play with corners touching a piece of the same color'

        return None # No problems

    def legal_moves(self, player, pieces):
        for c_piece in pieces:
            for piece in c_piece.orientations():
                for x in range(self.size):
                    for y in range(self.size):
                        location = x, y
                        if self._check_place_piece(piece, location, player) is None:
                            yield piece, location

    def in_bounds(self, point):
        x, y = point
        return (x >= 0 and y >= 0 and
                x < self.size and y < self.size)
