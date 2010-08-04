from poly import Poly, adjacent

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
        pieces = set(pieces)

        # Find available corners to play from.
        points_poly = Poly(p for p, v in self.data.items() if v == player)
        corners = set(points_poly.corner_adjacencies())
        if self.is_first(player):
            for p in self.start_points:
                if self.data.get(p) is None:
                    corners.add(p)

        # Find available space to play into.
        # Free space must not be occupied or next to a same-color piece.
        free_space = set()
        for x in range(self.size):
            for y in range(self.size):
                point = x, y
                if self.data.get(point) is not None:
                    continue
                if any(self.data.get(adj) == player
                       for adj in adjacent(point)):
                    continue
                free_space.add(point)
        corners &= free_space

        # Starting from the corners, grow successively larger possible plays.
        # First generation is just the size 1 polyomino on each corner.
        generations = [{Poly([c]) for c in corners}]
        max_size = max(len(p) for p in pieces)
        for gen_num in range(2, max_size + 1):
            old_gen = generations[-1]
            new_gen = set()
            # Add points to each polyomino in the last generation.
            for poly in old_gen:
                for adj in poly.adjacencies():
                    if adj in free_space:
                        new_gen.add(Poly(poly._points + (adj,)))
            generations.append(new_gen)

        for gen in generations:
            for piece in gen:
                if piece.canonical() not in pieces:
                    continue
                ###
                #reason = self._check_place_piece(piece, player, reason=True)
                #if reason is not None:
                #    self._place_piece(piece, player)
                #    assert False, '%s\n%s' % (reason, self)
                ###
                yield piece

    def in_bounds(self, point):
        x, y = point
        return (x >= 0 and y >= 0 and
                x < self.size and y < self.size)
