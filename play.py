#! /usr/bin/env python3

import itertools
import random
from copy import deepcopy
from pieces import all_pieces, piece_to_name, name_to_piece
from board import Board

def play_game(a, b, verbose=False):
    players = ['X', 'O']
    player_interfaces = {
        'X': a,
        'O': b,
    }
    player_pieces = {
        'X': deepcopy(all_pieces),
        'O': deepcopy(all_pieces),
    }

    board = Board()

    pass_count = 0
    for player in itertools.cycle(players):
        piece = player_interfaces[player].move(board, player, player_pieces)
        if piece is None: # Player passes
            pass_count += 1
            if pass_count >= len(players):
                break
            continue
        else:
            pass_count = 0
        available_pieces = player_pieces[player]
        c_piece = piece.canonical()
        if c_piece in available_pieces:
            available_pieces.remove(c_piece)
        else:
            raise ValueError('Piece not available.')
        board.place_piece(piece, player)
        if verbose:
            print(board)
            print()

    scores = {}
    for player in players:
        remaining = player_pieces[player]
        scores[player] = sum(len(piece) for piece in remaining)

    if verbose:
        print('game over')
        print('scores:')
        for player, score in scores.items():
            print('{} ({}) - {}'.format(player_interfaces[player].__name__, player, score))

        min_score = min(scores.values())
        for player, score in scores.items():
            if score == min_score:
                print('winner:', player_interfaces[player].__name__)

    return tuple(scores[p] for p in players)

def play_match(a, b, num_games, verbose=False):
    """
    Play the specified number of games, totaling scores.
    Randomize who goes first in the first match, and alternate thereafter.
    """
    scores_a = []
    scores_b = []
    random_first = random.choice((0, 1))
    for i in range(num_games):
        if (i + random_first) % 2 == 0:
            score_a, score_b = play_game(a, b, verbose)
        else:
            score_b, score_a = play_game(b, a, verbose)
        scores_a.append(score_a)
        scores_b.append(score_b)

    total_a = sum(scores_a)
    total_b = sum(scores_b)

    if verbose:
        print('match score:')
        print('{} - {}'.format(a.__name__, total_a))
        print('{} - {}'.format(b.__name__, total_b))

    return total_a, total_b

if __name__ == '__main__':
    import human
    import bot_null
    import bot_simple
    import bot_random
    import bot_biggest
    import bot_center
    import bot_corners
    import bot_efficiency

    bots = [
        human,
        bot_null,
        bot_simple,
        bot_random,
        bot_biggest,
        bot_center,
        bot_corners,
        bot_efficiency,
    ]

    import sys
    a_name = sys.argv[1]
    b_name = sys.argv[2]
    for bot in bots:
        if bot.__name__ == a_name:
            bot_a = bot
        if bot.__name__ == b_name:
            bot_b = bot

    num_rounds = 1
    if len(sys.argv) > 3:
        num_rounds = int(sys.argv[3])

    play_match(bot_a, bot_b, num_rounds, verbose=True)
