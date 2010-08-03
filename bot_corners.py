import random
from copy import deepcopy
from collections import defaultdict

from poly import Poly, adjacent

def free_corners(points, board, player):
    # Must be in bounds, unoccupied, and not next to any pieces of the same color.
    for corner in Poly(points).corner_adjacencies():
        if not board.in_bounds(corner):
            continue
        if board.data.get(corner):
            continue
        if any(board.data.get(adj) == player
               for adj in adjacent(corner)):
           continue
        yield corner

_placed_square_weight = 100
_free_corner_weight = 10
def evaluate(board, player, opponent):
    # Treat one player's pieces as a single polyomino to determine adjacencies.
    my_points = []
    their_points = []
    for point, color in board.data.items():
        if color == player:
            my_points.append(point)
        else:
            their_points.append(point)

    # Squares placed on board.
    squares_placed_score = (len(my_points) - len(their_points)) * _placed_square_weight

    # Free corners on board.
    my_corners = list(free_corners(my_points, board, player))
    their_corners = list(free_corners(their_points, board, opponent))
    free_corner_score = (len(my_corners) - len(their_corners)) * _free_corner_weight

    return squares_placed_score + free_corner_score

def move(board, player, player_pieces):
    opponents = list(player_pieces.keys())
    opponents.remove(player)
    opponent = opponents[0]
    moves = list(board.legal_moves(player, player_pieces[player]))
    if not moves:
        return
    moves_by_score = defaultdict(list)
    for piece in moves:
        temp_board = deepcopy(board)
        temp_board.place_piece(piece, player)
        score = evaluate(temp_board, player, opponent)
        moves_by_score[score].append(piece)
    max_score = max(moves_by_score.keys())
    return random.choice(moves_by_score[max_score])
