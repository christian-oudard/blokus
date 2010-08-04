from bots_base import make_move_func
from bots_library import placed_points, free_corners, fuzz

def distance(a, b):
    # Square distance, or Chebyshev distance.
    ax, ay = a
    bx, by = b
    return max(abs(bx - ax), abs(by - ay))

def centeredness(board, player, opponent):
    points = [p for p, v in board.data.items() if v == player]
    if not points:
        return 0
    center = (board.size - 1) / 2, (board.size - 1) / 2
    min_dist = sum(distance(p, center) for p in points) / len(points)
    return -min_dist

eval_funcs = [
    (placed_points, 100),
    (free_corners, 10),
    (centeredness, 8),
    (fuzz, 1),
]
move = make_move_func(eval_funcs)
