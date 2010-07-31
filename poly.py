# coding: utf8

import vec

class Poly:
    def __init__(self, data):
        self.data = data

    _block_char = '#'
    def __str__(self):
        """
        >>> p = Poly([(0, 0), (1, 0)])
        >>> print(p)
        ##
        """
        max_x = max(x for x, y in self.data)
        max_y = max(y for x, y in self.data)
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for x, y in self.data:
            grid[y][x] = self._block_char
        return '\n'.join(''.join(line) for line in grid)

    def canonicalize(self):
        """
        >>> p = Poly([(1, 1)])
        >>> p.canonicalize()
        >>> p.data
        [(0, 0)]
        >>> p = Poly([(-1, 1)])
        >>> p.canonicalize()
        >>> p.data
        [(0, 0)]
        """
        min_x = min(x for x, y in self.data)
        min_y = min(y for x, y in self.data)
        self.data = [vec.add(point, (-min_x, -min_y)) for point in self.data]
