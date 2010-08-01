import random

def move(board, player, player_pieces):
    moves = list(board.legal_moves(player, player_pieces[player]))
    if moves:
        return random.choice(moves)
