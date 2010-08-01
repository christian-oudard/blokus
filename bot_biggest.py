import random
from collections import defaultdict

def move(board, player, player_pieces):
    moves_by_size = defaultdict(list)
    for piece, location in board.legal_moves(player, player_pieces[player]):
        moves_by_size[len(piece)].append((piece, location))
    max_size = max(moves_by_size.keys())
    return random.choice(moves_by_size[max_size])
