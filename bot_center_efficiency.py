import random
from collections import defaultdict

from poly import Poly

def square_distance(a, b):
    ax, ay = a
    bx, by = b
    return max(abs(bx - ax), abs(by - ay))

def edge_efficiency(board, new_piece, player, opponent):
    # We want edge adjacencies, which can't be used, to be minimized, and
    # distributed efficiently. This means putting them on an opponent's piece,
    # off the board, or sharing them between pieces.

    score = 0
    new_adjs = set(new_piece.adjacencies())
    for adj in new_adjs:
        # Playing along board edges.
        if not board.in_bounds(adj):
            score += 1
        # Playing next to opponent pieces.
        if board.data.get(adj) == opponent:
            score += 1

    # Edges of the new piece that integrate with an existing piece.
    my_points = [p for p, v in board.data.items() if v == player]
    other_points = set(my_points) - set(new_piece)
    other_adjs = set(Poly(other_points).adjacencies())
    overlapping = other_adjs & new_adjs
    score += len(overlapping)

    return score

def evaluate(board, new_piece, player, opponent):
    # Score by the size of the piece.
    size_score = len(new_piece)

    # Each square in the polyomino gets points for how close to the center it is.
    center = (board.size - 1) / 2, (board.size - 1) / 2
    center_score = -max(square_distance(p, center) for p in new_piece)

    # Edge efficiency
    edge_score = edge_efficiency(board, new_piece, player, opponent)

    return (size_score, center_score + edge_score)

def move(board, player, player_pieces):
    opponents = list(player_pieces.keys())
    opponents.remove(player)
    opponent = opponents[0]

    moves = list(board.legal_moves(player, player_pieces[player]))
    if not moves:
        return
    moves_by_score = defaultdict(list)
    for piece in moves:
        evaluation = evaluate(board, piece, player, opponent)
        moves_by_score[evaluation].append(piece)
    max_score = max(moves_by_score.keys())
    return random.choice(moves_by_score[max_score])
