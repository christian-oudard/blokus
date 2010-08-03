from poly import Poly

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

    def place_piece(self, piece, color, reason=False):
        if reason:
            reason = self._check_place_piece(piece, color, reason=True)
            if reason is not None:
                raise ValueError(reason)
        else:
            if not self._check_place_piece(piece, color):
                raise ValueError('Invalid move')
        self._place_piece(piece, color)

    def _place_piece(self, piece, color):
        for point in piece:
            self.data[point] = color

    def _check_place_piece(self, piece, color, reason=False):
        # Check bounds.
        for point in piece:
            if not self.in_bounds(point):
                if reason:
                    return 'Piece out of bounds'
                return False
        # Check overlaps
        for point in piece:
            if point in self.data.keys():
                if reason:
                    return 'Overlapping pieces'
                return False
        # Check adjacencies.
        for adj in piece.adjacencies():
            if self.data.get(adj) == color:
                if reason:
                    return 'Cannot play next to a piece of the same color'
                return False

        if self.is_first(color):
            # Check start points.
            if not any(p in self.start_points for p in piece):
                if reason:
                    return 'Must play on a start point'
                return False
        else:
            # Check corner connections.
            if not any(
                self.data.get(corner) == color
                for corner in piece.corner_adjacencies()
            ):
                if reason:
                    return 'Must play with corners touching a piece of the same color'
                return False

        if reason:
            return None # No problems
        return True

    def legal_moves(self, player, pieces):
        if not pieces:
            return

        # Restrict search space to near the available corners.
        points_poly = Poly(p for p, v in self.data.items() if v == player)
        corners = list(points_poly.corner_adjacencies())
        if self.is_first(player):
            corners.extend(p for p in self.start_points if self.data.get(p) is None)
        min_x = min(x for x, y in corners)
        min_y = min(y for x, y in corners)
        max_x = max(x for x, y in corners)
        max_y = max(y for x, y in corners)
        max_piece_size = max(len(p) for p in pieces)
        x_range = range(
            max(0, min_x - max_piece_size + 1),
            min(self.size, max_x + 1),
        )
        y_range = range(
            max(0, min_y - max_piece_size + 1),
            min(self.size, max_y + 1),
        )
        locations = [(x, y) for x in x_range for y in y_range]
        #TODO: strip out locations by manhattan distance?
        for c_piece in pieces:
            for piece in c_piece.orientations():
                for x, y in locations:
                    t_piece = piece.translated(x, y)
                    #TODO check whether it hits any corners?
                    if self._check_place_piece(t_piece, player):
                        yield t_piece

    def in_bounds(self, point):
        x, y = point
        return (x >= 0 and y >= 0 and
                x < self.size and y < self.size)
