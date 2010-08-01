# coding: utf8

class Poly:
    def __init__(self, points):
        # Give points a predictable order.
        points = sorted(points)
        # Translate points to origin.
        min_x = min(x for x, y in points)
        min_y = min(y for x, y in points)
        self._points = tuple((x - min_x, y - min_y) for x, y in points)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._points)

    _block_char = '#'
    def __str__(self):
        """
        >>> p = Poly([(0, 0), (1, 0), (1, 1), (2, 1)])
        >>> print(p)
        ##
         ##
        """
        max_x = max(x for x, y in self._points)
        max_y = max(y for x, y in self._points)
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for x, y in self._points:
            grid[y][x] = self._block_char
        return '\n'.join(''.join(line).rstrip() for line in grid)

    def __eq__(self, other):
        return self._points == other._points

    def __hash__(self):
        """
        >>> {Poly([(0, 0)]), Poly([(0, 0)])}
        {Poly(((0, 0),))}
        """
        return hash((self.__class__, self._points))

    def __lt__(self, other):
        return ((len(self._points), self._points) <
                (len(other._points), other._points))

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
        clone = Poly(self._points)
        return min(clone.orientations())

    def orientations(self):
        """
        >>> p = Poly([(0, 0), (0, 1), (0, 2), (1, 0)])
        >>> for o in sorted(p.orientations()):
        ...     print(o)
        ...     print('----')
        ##
        #
        #
        ----
        #
        #
        ##
        ----
        ###
        #
        ----
        #
        ###
        ----
        ##
         #
         #
        ----
        ###
          #
        ----
          #
        ###
        ----
         #
         #
        ##
        ----
        """
        clone = Poly(self._points)
        rotations = [clone]
        for _ in range(3):
            rotations.append(Poly((y, -x) for x, y in rotations[-1]._points))
        mirrors = []
        for r in rotations:
            mirrors.append(Poly((x, -y) for x, y in r._points))
        return set(rotations + mirrors)

    def adjacencies(self):
        """
        >>> p = Poly([(0, 0), (1, 0)])
        >>> sorted(p.adjacencies())
        [(-1, 0), (0, -1), (0, 1), (1, -1), (1, 1), (2, 0)]
        """
        for point in self._points:
            for adj in adjacent(point):
                if adj not in self._points:
                    yield adj


def adjacent(point):
    """
    >>> sorted(adjacent((1, 1)))
    [(0, 1), (1, 0), (1, 2), (2, 1)]
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
    ##
    ##
    ----
    #
    ##
     #
    ----
    """
    if generation == 1:
        return {Poly([(0, 0)])}

    new_polys = set()
    for poly in gen_polys(generation - 1):
        for adj in poly.adjacencies():
            new_poly = Poly(poly._points + (adj,))
            new_polys.add(new_poly.canonical())
    return new_polys
