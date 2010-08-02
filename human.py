import sys
from copy import deepcopy
from getch import getch, getch_arrow
from pieces import piece_to_name, name_to_piece

def display_board(board, player):
    from term_colors import print_color, rgb, gray

    orange = rgb(5, 2, 0)
    purple = rgb(3, 0, 4)
    colors = {
        'X': orange,
        'O': purple,
    }
    dark_gray = gray(5)
    light_gray = gray(15)
    black = gray(0)

    print('+' + '='*board.size*2 + '+')
    for y in range(board.size):
        print('|', end='')
        for x in range(board.size):
            d = board.data.get((x, y))
            bg = colors.get(d, dark_gray)
            fg = light_gray
            if (x, y) in board.start_points and d is None:
                s = '()'
            else:
                s = '  '
            if d in ['#', '@']:
                bg = colors[player]
            if d == '#':
                s = '><'
                fg = black
            print_color(s, bg=bg, fg=fg, end='')
        print('|')

    print('+' + '='*board.size*2 + '+')



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

def move(board, player, player_pieces):
    print("{}'s turn.".format(player))

    display_board(board, player)

    # Choose piece.
    my_pieces = player_pieces[player]
    while True:
        name = get_input('piece? >')
        piece = name_to_piece.get(name)
        if not piece:
            print('Piece name not recognized.')
        elif piece not in my_pieces:
            piece = None
            print('You have already played this piece.')
        else:
            break
        print('Available pieces:',
              ', '.join(piece_to_name[p] for p in player_pieces[player]))

    # Choose orientation.
    orientations = sorted(piece.orientations())
    piece = orientations[0]
    o_index = 0

    # Place piece
    location = board.size // 2, board.size // 2
    while True:
        temp_board = deepcopy(board)
        reason = temp_board._check_place_piece(piece, location, player)
        if reason is not None:
            color = '#'
        else:
            color = '@'
        temp_board._place_piece(piece, location, color)
        display_board(temp_board, player)

        if reason is not None:
            print('** {} **'.format(reason))

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

        # Go back.
        if command == '\x1b': # Escape key
            pass #STUB, go back to piece selection.

        # Confirm.
        if command == '\r': # Enter key
            if reason is None:
                return piece, location
