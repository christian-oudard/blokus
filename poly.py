# coding: utf8

class Poly:
    def __init__(self, points):
        # Give points a predictable order.
        points = sorted(points)
        # Translate points to origin.
        min_x = min(x for x, y in points)
        min_y = min(y for x, y in points)
        self._points = tuple(translate(points, -min_x, -min_y))

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

    def __len__(self):
        return len(self._points)

    def __eq__(self, other):
        return isinstance(other, Poly) and self._points == other._points

    def __hash__(self):
        """
        >>> {Poly([(0, 0)]), Poly([(0, 0)])}
        {Poly(((0, 0),))}
        """
        return hash((self.__class__, self._points))

    def __lt__(self, other):
        return ((len(self), self._points) <
                (len(other), other._points))

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

def translate(points, tx, ty):
    for x, y in points:
        yield x + tx, y + ty

def adjacencies(points):
    """
    >>> points = [(0, 0), (0, 1), (1, 0)]
    >>> print(Poly(points))
    ##
    #
    >>> adjs = list(adjacencies(points))
    >>> len(adjs)
    7
    >>> print(Poly(adjs))
     ##
    #  #
    # #
     #
    """
    points = set(points)
    for x, y in list(points):
        for adj in [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]:
            if adj not in points:
                yield adj
                points.add(adj)

def corner_adjacencies(points):
    """
    >>> points = [(0, 0), (1, 0), (1, 1), (2, 1)]
    >>> print(Poly(points))
    ##
     ##
    >>> adjs = list(corner_adjacencies(points))
    >>> len(adjs)
    6
    >>> print(Poly(adjs))
    #  #
        #
    #
     #  #
    """
    adjs = set(adjacencies(points))
    points = set(points)
    for x, y in list(points):
        for adj in [
            (x - 1, y - 1),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x + 1, y + 1),
        ]:
            if adj not in points and \
               adj not in adjs:
                yield adj
                points.add(adj)


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
        points = poly._points
        for adj in adjacencies(points):
            new_poly = Poly(points + (adj,))
            new_polys.add(new_poly.canonical())
    return new_polys
