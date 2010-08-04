from copy import deepcopy

def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 1
    return (value - min_val) / (max_val - min_val)

def make_move_func(eval_funcs, debug=False):
    def move_func(board, player, player_pieces):
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
                (func(temp_board, player, opponent) -
                 func(temp_board, opponent, player))
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
    return move_func
