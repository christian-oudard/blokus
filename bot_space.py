import random
from copy import deepcopy
from collections import defaultdict

from poly import adjacent

def available_space(board, player, opponent):
    # Free space must not be occupied or next to a same-color piece.
    space = 0
    for x in range(board.size):
        for y in range(board.size):
            point = x, y
            if board.data.get(point):
                continue
            if any(board.data.get(adj) == player
                   for adj in adjacent(point)):
                continue
            space += 1
    return space

def evaluate(board, player, opponent):
    # Treat one player's pieces as a single polyomino to determine adjacencies.
    my_points = []
    their_points = []
    for point, color in board.data.items():
        if color == player:
            my_points.append(point)
        else:
            their_points.append(point)

    # Squares placed on board.
    squares_placed_score = (len(my_points) - len(their_points))

    # Available space.
    my_space = available_space(board, player, opponent)
    their_space = available_space(board, opponent, player)
    space_score = my_space - their_space

    return (squares_placed_score, space_score)

def move(board, player, player_pieces):
    opponents = list(player_pieces.keys())
    opponents.remove(player)
    opponent = opponents[0]
    moves = list(board.legal_moves(player, player_pieces[player]))
    if not moves:
        return
    moves_by_score = defaultdict(list)
    for piece in moves:
        temp_board = deepcopy(board)
        temp_board.place_piece(piece, player)
        score = evaluate(temp_board, player, opponent)
        moves_by_score[score].append(piece)
    max_score = max(moves_by_score.keys())
    return random.choice(moves_by_score[max_score])

