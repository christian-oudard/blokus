import random
from collections import defaultdict
from poly import translate

def manhattan_distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(bx - ax) + abs(by - ay)

def evaluate(board, piece, location):
    # Score by the size of the piece.
    size_score = len(piece)

    # Each square in the polyomino gets points for how close to the center it is.
    center_score = 0
    center = board.size / 2, board.size / 2
    max_dist = manhattan_distance((0, 0), center)
    points = translate(piece._points, *location)
    for p in points:
        d = manhattan_distance(p, center)
        center_score += (max_dist - d)
    return (size_score, center_score)

def move(board, player, player_pieces):
    moves = list(board.legal_moves(player, player_pieces[player]))
    if not moves:
        return
    moves_by_score = defaultdict(list)
    for piece, location in moves:
        moves_by_score[evaluate(board, piece, location)].append((piece, location))
    max_score = max(moves_by_score.keys())
    return random.choice(moves_by_score[max_score])
