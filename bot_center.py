import random
from collections import defaultdict

def manhattan_distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(bx - ax) + abs(by - ay)

def evaluate(board, piece):
    # Each square in the polyomino gets points for how close to the center it is.
    center = board.size / 2, board.size / 2
    max_dist = manhattan_distance((0, 0), center)
    score = 0
    for p in piece:
        d = manhattan_distance(p, center)
        score += (max_dist - d)
    return score

def move(board, player, player_pieces):
    moves = list(board.legal_moves(player, player_pieces[player]))
    if not moves:
        return
    moves_by_score = defaultdict(list)
    for piece in moves:
        moves_by_score[evaluate(board, piece)].append(piece)
    max_score = max(moves_by_score.keys())
    return random.choice(moves_by_score[max_score])
