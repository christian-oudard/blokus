#! /usr/bin/env python3

import sys
import itertools
from copy import deepcopy
from pieces import all_pieces, piece_to_name, name_to_piece
from board import Board
from getch import getch, getch_arrow

def display_board(board):
    print('+' + '='*board.size + '+')
    for line in str(board).split('\n'):
        print('|' + line + '|')
    print('+' + '='*board.size + '+')

def get_input(prompt):
    if not prompt[-1].isspace():
        prompt += ' '
    while True:
        try:
            command = input(prompt)
            if command == 'exit':
                sys.exit()
            return command
        except (KeyboardInterrupt, EOFError):
            print()
            confirmation = input('Are you sure you want to exit [Y / N]? ')
            if confirmation.lower().startswith('y'):
                sys.exit()

if __name__ == '__main__':
    players = ['X', 'O']
    player_pieces = {
        'X': deepcopy(all_pieces),
        'O': deepcopy(all_pieces),
    }

    board = Board()

    for player in itertools.cycle(players):
        display_board(board)
        print("{}'s turn.".format(player))

        # Choose piece.
        while True:
            name = get_input('piece? >')
            piece = name_to_piece.get(name)
            if piece:
                break
            print('Piece name not recognized. Available pieces:',
                  ', '.join(piece_to_name[p] for p in player_pieces[player]))

        # Choose orientation.
        orientations = sorted(piece.orientations())
        piece = orientations[0]
        o_index = 0

        # Place piece
        location = board.size // 2, board.size // 2
        while True:
            temp_board = deepcopy(board)
            try:
                temp_board._check_place_piece(piece, location, player)
            except ValueError as e:
                print(e)
                color = '#'
            else:
                color = '@'
            temp_board._place_piece(piece, location, color)
            display_board(temp_board)

            print('Use arrow keys to move piece. Press space bar to change orientation. Press Enter to confirm, or escape to go back (STUB).')

            command = getch_arrow()

            if command == '\x03': # Ctrl-C
                raise KeyboardInterrupt()

            # Change location
            x, y = location
            if command == 'up':
                y -= 1
            if command == 'down':
                y += 1
            if command == 'left':
                x -= 1
            if command == 'right':
                x += 1
            x %= board.size
            y %= board.size
            location = x, y

            # Change orientation.
            if command == ' ': # Space key
                o_index = (o_index + 1) % len(orientations)
                piece = orientations[o_index]

            # Confirm.
            if command == '\r': # Enter key
                try:
                    board.place_piece(piece, location, player)
                except ValueError as e:
                    print('Cannot place piece here.')
                else:
                    break

            # Go back.
            if command == '\x1b': # Escape key
                pass #STUB, go back to piece selection.


