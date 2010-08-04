import random
from poly import Poly, adjacent

def fuzz(board, player, opponent):
    return random.uniform(0, 1)

def placed_points(board, player, opponent):
    score = 0
    for value in board.data.values():
        if value == player:
            score += 1
    return score

def free_corners(board, player, opponent):
    score = 0
    points = [p for p, v in board.data.items() if v == player]
    # Must be in bounds, unoccupied, and not next to any pieces of the same color.
    for corner in Poly(points).corner_adjacencies():
        if not board.in_bounds(corner):
            continue
        if board.data.get(corner):
            continue
        if any(board.data.get(adj) == player
               for adj in adjacent(corner)):
           continue
        score += 1
    return score

