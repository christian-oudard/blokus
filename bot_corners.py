from bot_base import make_move_func
from bots_library import placed_points, free_corners, fuzz

eval_funcs = [
    (placed_points, 100),
    (free_corners, 10),
    (fuzz, 2),
]
move = make_move_func(eval_funcs)
