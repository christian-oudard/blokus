from poly import translate, adjacencies, corner_adjacencies

class Board:
    _empty = '.'
    _start = 'o'
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
            grid[y][x] = color
        return '\n'.join(''.join(line) for line in grid)

    def is_first(self, color):
        return not any(v == color for v in self.data.values())

    def place_piece(self, piece, position, color):
        points = list(translate(piece._points, *position))
        # Check bounds.
        for x, y in points:
            if x < 0 or y < 0 or  x >= self.size or y >= self.size:
                raise ValueError('Piece out of bounds')
        # Check overlaps
        for point in points:
            if point in self.data.keys():
                raise ValueError('Overlapping pieces')
        # Check adjacencies.
        for adj in adjacencies(points):
            if self.data.get(adj) == color:
                raise ValueError('Cannot play next to a piece of the same color')

        if self.is_first(color):
            # Check start points.
            if not any(p in self.start_points for p in points):
                raise ValueError('Must play on a start point')
        else:
            # Check corner connections.
            if not any(
                self.data.get(corner) == color
                for corner in corner_adjacencies(points)
            ):
                raise ValueError('Must play with corners touching a piece of the same color')

        # All checks pass, place the piece.
        for point in points:
            self.data[point] = color
