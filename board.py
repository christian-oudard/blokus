from poly import translate, adjacencies, corner_adjacencies

_empty = '.'
class Board:
    size = 14
    start_positions = (
        (4, 4),
        (9, 9),
    )
    def __init__(self):
        self.data = {}

    def __str__(self):
        grid = [[_empty for _ in range(self.size)] for _ in range(self.size)]
        for point, color in self.data.items():
            x, y = point
            grid[y][x] = color
        return '\n'.join(''.join(line) for line in grid)

    def is_first(self, color):
        return not any(v == color for v in self.data.values())

    def place_piece(self, piece, position, color):
        points = list(translate(piece._points, *position))

        for adj in adjacencies(points):
            if self.data.get(adj) == color:
                raise ValueError('Cannot play next to a piece of the same color')

        if self.is_first(color):
            pass #STUB, must play on a start position
        elif not any(
            self.data.get(corner) == color
            for corner in corner_adjacencies(points)
        ):
            raise ValueError('Must play with corners touching a piece of the same color')

        for point in points:
            x, y = point
            if x < 0 or y < 0 or  x >= self.size or y >= self.size:
                raise ValueError('Piece out of bounds')
            if point in self.data:
                raise ValueError('Overlapping pieces')
            self.data[point] = color
