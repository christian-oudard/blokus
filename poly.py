class Poly:
    def __init__(self, points):
        # Give points a predictable order.
        self._points = tuple(sorted(points))

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
        max_x = max(x for x, y in self)
        max_y = max(y for x, y in self)
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for x, y in self:
            grid[y][x] = self._block_char
        return '\n'.join(''.join(line).rstrip() for line in grid)

    def __len__(self):
        return len(self._points)

    def __iter__(self):
        return iter(self._points)

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

    def translate_origin(self):
        min_x = min(x for x, y in self)
        min_y = min(y for x, y in self)
        return self.translated(-min_x, -min_y)

    def translated(self, tx, ty):
        return Poly((x + tx, y + ty) for x, y in self)

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
        clone = Poly(self)
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
        clone = Poly(self)
        rotations = [clone]
        for _ in range(3):
            rotations.append(Poly((y, -x) for x, y in rotations[-1]))
        mirrors = []
        for r in rotations:
            mirrors.append(Poly((x, -y) for x, y in r))
        orientations = rotations + mirrors
        orientations = set(p.translate_origin() for p in orientations)
        return orientations

    def adjacencies(self):
        """
        >>> poly = Poly([(0, 0), (0, 1), (1, 0)])
        >>> print(poly)
        ##
        #
        >>> adjs = list(poly.adjacencies())
        >>> len(adjs)
        7
        >>> print(Poly(adjs).translate_origin())
         ##
        #  #
        # #
         #
        """
        points = set(self)
        for x, y in list(points):
            for adj in adjacent((x, y)):
                if adj not in points:
                    yield adj
                    points.add(adj)

    def corner_adjacencies(self):
        """
        >>> poly = Poly([(0, 0), (1, 0), (1, 1), (2, 1)])
        >>> print(poly)
        ##
         ##
        >>> adjs = list(poly.corner_adjacencies())
        >>> len(adjs)
        6
        >>> print(Poly(adjs).translate_origin())
        #  #
            #
        #
         #  #
        """
        adjs = set(self.adjacencies())
        points = set(self)
        for x, y in self:
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
        for adj in poly.adjacencies():
            new_poly = Poly(poly._points + (adj,))
            new_polys.add(new_poly.canonical())
    return new_polys

def adjacent(point):
    x, y = point
    return [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]
