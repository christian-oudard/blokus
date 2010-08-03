import random
from copy import deepcopy
from collections import defaultdict

from poly import Poly

def edge_efficiency(board, new_piece, points, player, opponent):
    # We want edge adjacencies, which can't be used, to be minimized, and
    # distributed efficiently. This means putting them on an opponent's piece,
    # off the board, or sharing them between pieces.

    score = 0
    adjacency_set = set(Poly(points).adjacencies())
    for adj in adjacency_set:
        # Playing along board edges.
        if not board.in_bounds(adj):
            score += 1
        # Playing next to opponent pieces.
        if board.data.get(adj) == opponent:
            score += 1

    # Edges of the new piece that integrate with an existing piece.
    other_points = set(points) - set(new_piece)
    other_adjs = set(Poly(other_points).adjacencies())
    new_adjs = set(new_piece.adjacencies())
    overlapping = other_adjs & new_adjs
    score += len(overlapping)

    return score

def evaluate(board, new_piece, player, opponent):
    # Treat one player's pieces as a single polyomino to determine adjacencies.
    my_points = []
    their_points = []
    for point, color in board.data.items():
        if color == player:
            my_points.append(point)
        else:
            their_points.append(point)

    # Squares placed on board.
    squares_placed_score = (len(my_points) - len(their_points))

    # Edge efficiency
    edge_score = edge_efficiency(board, new_piece, my_points, player, opponent)

    return (squares_placed_score, edge_score)

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
        score = evaluate(temp_board, piece, player, opponent)
        moves_by_score[score].append(piece)
    max_score = max(moves_by_score.keys())
    print(max_score)
    return random.choice(moves_by_score[max_score])

