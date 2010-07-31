# coding: utf8

import vec

class Poly:
    def __init__(self, data):
        self._data = tuple(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._data)

    _block_char = '#'
    def __str__(self):
        """
        >>> p = Poly([(0, 0), (1, 0)])
        >>> print(p)
        ##
        """
        max_x = max(x for x, y in self._data)
        max_y = max(y for x, y in self._data)
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for x, y in self._data:
            grid[y][x] = self._block_char
        return '\n'.join(''.join(line) for line in grid)

    def canonical(self):
        """
        Return the canonical form of the polyomino.

        Canonical forms of polyominos have several properties.
        The points are translated to the axes:
        >>> p = Poly([(1, 1)])
        >>> p.canonical()
        Poly(((0, 0),))
        >>> p = Poly([(-1, 1)])
        >>> p.canonical()
        Poly(((0, 0),))

        Their point order is deterministic:
        >>> p = Poly([(0, 0), (0, 1)])
        >>> p.canonical()
        Poly(((0, 0), (0, 1)))
        >>> p = Poly([(0, 1), (0, 0)])
        >>> p.canonical()
        Poly(((0, 0), (0, 1)))

        """
        clone = Poly(sorted(self._data))
        min_x = min(x for x, y in self._data)
        min_y = min(y for x, y in self._data)
        clone._data = tuple(vec.add(point, (-min_x, -min_y)) for point in clone._data)

        #TODO: rotation
        #TODO: mirroring
        return clone

    def __eq__(self, other):
        return self._data == other._data

    def __hash__(self):
        """
        >>> {Poly([(0, 0)]), Poly([(0, 0)])}
        {Poly(((0, 0),))}
        """
        return hash((self.__class__, self._data))
