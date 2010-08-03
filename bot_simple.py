def move(board, player, player_pieces):
    for piece in list(board.legal_moves(player, player_pieces[player])):
        return piece
