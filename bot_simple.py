from copy import deepcopy

def move(board, player, player_pieces):
    for piece, location in board.legal_moves(player, player_pieces[player]):
        return piece, location
