import sys
from copy import deepcopy
from getch import getch, getch_arrow
from poly import piece_to_name, name_to_piece

def display_board(board, player):
    from term_colors import print_color, rgb, gray

    orange = rgb(5, 2, 0)
    purple = rgb(3, 0, 4)
    colors = {
        'X': orange,
        'O': purple,
    }
    light_gray = gray(15)
    black = gray(0)

    print('+' + '='*board.size*2 + '+')
    for y in range(board.size):
        print('|', end='')
        for x in range(board.size):
            d = board.data.get((x, y))
            bg = colors.get(d, None)
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

def choose_piece(my_pieces):
    while True:
        print('Available pieces:',
              ', '.join(piece_to_name[p] for p in my_pieces))
        name = get_input('Choose a piece, or type "pass":')
        name = name.lower()
        if name == 'pass':
            return 'pass'
        piece = name_to_piece.get(name)
        if not piece:
            print('Piece name not recognized.')
        elif piece not in my_pieces:
            print('You have already played this piece.')
        else:
            return piece

def choose_placement(board, piece, player):
    orientations = sorted(piece.orientations())
    piece = orientations[0]
    o_index = 0

    location = board.size // 2, board.size // 2
    while True:
        t_piece = piece.translated(*location)
        temp_board = deepcopy(board)
        reason = temp_board._check_place_piece(t_piece, player, reason=True)
        if reason is not None:
            color = '#'
        else:
            color = '@'
        temp_board._place_piece(t_piece, color)
        display_board(temp_board, player)

        if reason is not None:
            print('** {} **'.format(reason))

        print('Use arrow keys to move piece. Press space bar to change orientation.')
        print('Press Enter to confirm move, or backspace to go back.')

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
        if command == '\x7f': # Backspace key
            return None # Go back to piece selection.

        # Confirm.
        if command == '\r': # Enter key
            if reason is None:
                return t_piece

def move(board, player, player_pieces):
    print("{}'s turn.".format(player))

    while True:
        display_board(board, player)

        piece = choose_piece(player_pieces[player])
        if piece == 'pass':
            return None

        t_piece = choose_placement(board, piece, player)
        if t_piece is None:
            continue # User chose to re-choose piece.

        return t_piece
