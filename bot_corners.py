import random
from copy import deepcopy

from poly import Poly, adjacent

def placed_points(board, player, opponent):
    score = 0
    for value in board.data.values():
        if value == player:
            score += 1
    return score

def free_corners(board, player, opponent):
    score = 0
    points = [p for p, v in board.data.items() if v == player]
    # Must be in bounds, unoccupied, and not next to any pieces of the same color.
    for corner in Poly(points).corner_adjacencies():
        if not board.in_bounds(corner):
            continue
        if board.data.get(corner):
            continue
        if any(board.data.get(adj) == player
               for adj in adjacent(corner)):
           continue
        score += 1
    return score

def fuzz(board, player, opponent):
    return random.uniform(0, 1)

eval_funcs = [
    (placed_points, 100),
    (free_corners, 10),
    (fuzz, 0),
]

def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 1
    return (value - min_val) / (max_val - min_val)

def move(board, player, player_pieces, debug=False):
    if not player_pieces:
        return
    opponents = list(player_pieces.keys())
    opponents.remove(player)
    opponent = opponents[0]

    # Run each evaluation function on each move.
    moves = list(board.legal_moves(player, player_pieces[player]))
    if not moves:
        return
    move_evals = {}
    for piece in moves:
        temp_board = deepcopy(board)
        temp_board.place_piece(piece, player)
        move_evals[piece] = tuple(
            func(temp_board, player, opponent)
            for func, weight in eval_funcs
        )

    # Normalize evaluation functions to range [0, 1]
    func_spans = []
    for i in range(len(eval_funcs)):
        min_score = min(score[i] for move, score in move_evals.items())
        max_score = max(score[i] for move, score in move_evals.items())
        func_spans.append((min_score, max_score))
    normalized_scores = {}
    for piece in moves:
        scores = move_evals[piece]
        normalized_scores[piece] = tuple(
            normalize(score, max_val, min_val)
            for score, (max_val, min_val) in zip(scores, func_spans)
        )
    # Add in weights.
    pieces_by_score = {}
    for piece in moves:
        score = 0
        n_scores = normalized_scores[piece]
        for n_score, (eval_func, weight) in zip(n_scores, eval_funcs):
            score += n_score * weight
        pieces_by_score[score] = piece
    max_score = max(pieces_by_score.keys())
    move = pieces_by_score[max_score]

    if debug:
        print(', '.join('{} x{}'.format(f.__name__, m) for f, m in eval_funcs))
        print('raw evals', move_evals[move])
        print('span', func_spans)
        print('normalized', normalized_scores[move])
        print('weighted', ' + '.join(
            str(n_score * weight)
            for n_score, (eval_func, weight)
            in zip(normalized_scores[move], eval_funcs)
        ))
        print('total', max_score)
    return move
