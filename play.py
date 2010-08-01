#! /usr/bin/env python3

import itertools
from copy import deepcopy
from pieces import all_pieces, piece_to_name, name_to_piece
from board import Board

if __name__ == '__main__':
    import human

    players = ['X', 'O']
    player_interfaces = {
        'X': human,
        'O': human,
    }
    player_pieces = {
        'X': deepcopy(all_pieces),
        'O': deepcopy(all_pieces),
    }

    board = Board()

    for player in itertools.cycle(players):
        piece, location = player_interfaces[player].move(board, player, player_pieces)
        available_pieces = player_pieces[player]
        c_piece = piece.canonical()
        if c_piece in available_pieces:
            available_pieces.remove(c_piece)
        else:
            raise ValueError('Piece not available.')
        board.place_piece(piece, location, player)
