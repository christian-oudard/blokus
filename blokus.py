from poly import Poly, gen_polys

max_size = 5
pieces = []
for size in range(1, max_size + 1):
    pieces.extend(gen_polys(size))
pieces.sort(key=lambda p: (len(p._points), p))
