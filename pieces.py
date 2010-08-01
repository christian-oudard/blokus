from poly import Poly, gen_polys

_max_size = 5
all_pieces = []
for size in range(1, _max_size + 1):
    all_pieces.extend(gen_polys(size))
all_pieces.sort()

one = Poly([(0, 0),])
#

two = Poly([(0, 0), (0, 1)])
#
#

three_i = Poly([(0, 0), (0, 1), (0, 2)])
#
#
#

three_l = Poly([(0, 0), (0, 1), (1, 0)])
#
##

four_i = Poly([(0, 0), (0, 1), (0, 2), (0, 3)])
#
#
#
#

four_l = Poly([(0, 0), (0, 1), (0, 2), (1, 0)])
#
#
##

four_t = Poly([(0, 0), (0, 1), (0, 2), (1, 1)])
###
#

four_o = Poly([(0, 0), (0, 1), (1, 0), (1, 1)])
##
##

four_s = Poly([(0, 0), (0, 1), (1, 1), (1, 2)])
##
##

five_i = Poly([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])
#
#
#
#
#

five_l = Poly([(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)])
#
#
#
##

five_y = Poly([(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)])
#
##
#
#

five_p = Poly([(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)])
##
##
#

five_u = Poly([(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)])
# #
###

five_v = Poly([(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)])
#
#
###

five_t = Poly([(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)])
###
#
#

five_j = Poly([(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)])
#
#
##
#

five_f = Poly([(0, 0), (0, 1), (1, 1), (1, 2), (2, 1)])
##
##
#

five_w = Poly([(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)])
#
##
##

five_z = Poly([(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)])
##
#
##

five_x = Poly([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)])
 #
###
 #

# Put them in an index dictionary too.
piece_to_name = {}
name_to_piece = {}
for k, v in dict(locals()).items():
    if isinstance(v, Poly):
        name_to_piece[k] = v
        piece_to_name[v] = k
assert len(name_to_piece) == len(all_pieces)
assert len(piece_to_name) == len(all_pieces)
