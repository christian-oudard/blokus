def evaluate(board, piece, location):
    # Score by the size of the piece.
    return len(piece)

def move_by_evaluation(eval_func):
    def move(board, player, player_pieces):
        moves = list(board.legal_moves(player, player_pieces[player]))
        if not moves:
            return
        moves_by_score = defaultdict(list)
        for piece, location in moves:
            moves_by_score[eval_func(board, piece, location)].append((piece, location))
        max_score = max(moves_by_score.keys())
        return random.choice(moves_by_score[max_score])
    return move
move = move_by_evaluation(evaluate)
