# coding: utf8

def _translate_origin(points):
    min_x = min(x for x, y in points)
    min_y = min(y for x, y in points)
    for x, y in points:
        yield (x - min_x, y - min_y)

class Poly:
    def __init__(self, data):
        self._data = tuple(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._data)

    _block_char = '#'
    def __str__(self):
        """
        >>> p = Poly([(0, 0), (1, 0), (1, 1), (2, 1)])
        >>> print(p)
        ##
         ##
        """
        max_x = max(x for x, y in self._data)
        max_y = max(y for x, y in self._data)
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for x, y in self._data:
            grid[y][x] = self._block_char
        return '\n'.join(''.join(line).rstrip() for line in grid)

    def __eq__(self, other):
        return self._data == other._data

    def __hash__(self):
        """
        >>> {Poly([(0, 0)]), Poly([(0, 0)])}
        {Poly(((0, 0),))}
        """
        return hash((self.__class__, self._data))

    def __lt__(self, other):
        return self._data < other._data

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

        Their rotation is irrelevant:
        >>> p = Poly([(0, 0), (0, 1)])
        >>> print(p)
        #
        #
        >>> print(p.canonical())
        #
        #
        >>> p = Poly([(0, 0), (1, 0)])
        >>> print(p)
        ##
        >>> print(p.canonical())
        #
        #
        """
        clone = Poly(self._data)

        # Translation and sorting.
        clone._data = tuple(sorted(_translate_origin(clone._data)))

        # Choose the best rotation.
        rotations = [clone]
        for _ in range(3):
            rotations.append(rotations[-1].rotated_right())
        clone = min(rotations)

        #TODO: mirroring

        return clone


    def rotated_right(self):
        """
        >>> p = Poly([(0, 0), (1, 0), (1, 1), (2, 1)])
        >>> p
        Poly(((0, 0), (1, 0), (1, 1), (2, 1)))
        >>> print(p)
        ##
         ##
        >>> p.rotated_right()
        Poly(((0, 1), (0, 2), (1, 0), (1, 1)))
        >>> print(p.rotated_right())
         #
        ##
        #
        """
        clone = Poly(self._data)
        clone._data = tuple(sorted((y, -x) for x, y in clone._data))
        clone._data = tuple(_translate_origin(clone._data))
        return clone


def adjacent(point):
    """
    >>> list(adjacent((1, 1)))
    [(0, 1), (2, 1), (1, 0), (1, 2)]
    """
    x, y = point
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y - 1)
    yield (x, y + 1)

def gen_polys(generation):
    """
    >>> for poly in sorted(gen_polys(2)):
    ...     print(poly)
    ...     print('----')
    #
    #
    ----
    >>> for poly in sorted(gen_polys(3)):
    ...     print(poly)
    ...     print('----')
    #
    #
    #
    ----
    ##
    #
    ----
    >>> for poly in sorted(gen_polys(4)):
    ...     print(poly)
    ...     print('----')
    #
    #
    #
    #
    ----
    ##
    #
    #
    ----
    #
    ##
    #
    ----
    #
    #
    ##
    ----
    ##
    ##
    ----
    #
    ##
     #
    ----
    ##
     ##
    ----
    """
    if generation == 1:
        return {Poly([(0, 0)])}

    new_polys = set()
    for poly in gen_polys(generation - 1):
        data = poly._data
        for point in data:
            for adj in adjacent(point):
                if adj not in data:
                    new_poly = Poly(data + (adj,))
                    new_polys.add(new_poly.canonical())
    return new_polys
