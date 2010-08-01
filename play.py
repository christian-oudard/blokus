#! /usr/bin/env python3

import itertools
from copy import deepcopy
from pieces import all_pieces, piece_to_name, name_to_piece
from board import Board

if __name__ == '__main__':
    import human
    import bot_simple
    import bot_random
    import bot_biggest

    players = ['X', 'O']
    player_interfaces = {
        'X': bot_random,
        'O': bot_biggest,
    }
    player_pieces = {
        'X': deepcopy(all_pieces),
        'O': deepcopy(all_pieces),
    }

    board = Board()

    pass_count = 0
    for player in itertools.cycle(players):
        move = player_interfaces[player].move(board, player, player_pieces)
        if move is None: # Player passes
            pass_count += 1
            if pass_count >= len(players):
                break
            continue
        piece, location = move
        available_pieces = player_pieces[player]
        c_piece = piece.canonical()
        if c_piece in available_pieces:
            available_pieces.remove(c_piece)
        else:
            raise ValueError('Piece not available.')
        board.place_piece(piece, location, player)
        print(board)
        print()

    scores = {}
    for player in players:
        remaining = player_pieces[player]
        scores[player] = sum(len(piece) for piece in remaining)

    print('game over')
    print('scores:')
    for player, score in scores.items():
        print('{} - {}'.format(player, score))

    min_score = min(scores.values())
    for player, score in scores.items():
        if score == min_score:
            print('winner:', player)
