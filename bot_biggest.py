def evaluate(board, piece, location):
    # Score by the size of the piece.
    return len(piece)

from bots_utility import move_by_evaluation
move = move_by_evaluation(evaluate)
