from poly import translate, adjacencies

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
        points = list(translate(piece._points, *position))
        for adj in adjacencies(points):
            if self.data.get(adj) == color:
                raise ValueError('Cannot play next to a piece of the same color.')
        for point in points:
            x, y = point
            if x < 0 or y < 0 or  x >= self.size or y >= self.size:
                raise ValueError('Piece out of bounds')
            if point in self.data:
                raise ValueError('Overlapping pieces')
            self.data[point] = color