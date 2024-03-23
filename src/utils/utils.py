import bisect
import math
import random
import sys
from random import random as rand
from typing import List, Tuple

import numpy as np

from src.utils.bounding import Bounding


def random_from_seed(seed: int) -> float:
    rnd = random.Random(seed)
    return rnd.random()


def random_from_seed_in_range(x1: float, x2: float, seed: int) -> float:
    rnd = random.Random(seed)
    return (x2 - x1) * rnd.random() + x1


def get_randomizer(seed: int) -> object:
    return random.Random(seed)


def random_color():
    return int(255 * rand()), int(255 * rand()), int(255 * rand())


def get_quad_dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def get_random_seed() -> int:
    return math.floor(rand() * 2**32)


def get_position_seed(x: int, y: int, seed: int = 0) -> int:
    """ Returns unique seed for discrete positions by adding spiral-like unique value to specified seed. """
    max_abs = max(abs(x), abs(y))
    inner_spiral_width = 2 * max_abs - 1
    spiral_width = inner_spiral_width + 1
    addition = inner_spiral_width * inner_spiral_width
    if max_abs == abs(x):
        if x > 0:
            addition += y + max_abs  # right
        else:
            addition += spiral_width + y + max_abs  # left
    else:
        if y > 0:
            addition += 2 * spiral_width + x + max_abs  # top
        else:
            addition += 3 * spiral_width + x + max_abs  # bottom
    return (seed + addition) % (2**32)


def is_power_of_two(x: int) -> bool:
    return (x & (x-1) == 0) and x != 0


def get_cumulative_distribution_list(weights: List[float]) -> List[float]:
    cumulative_distribution = []
    cur_summ = 0
    for w in weights:
        cur_summ += w
        cumulative_distribution.append(cur_summ)
    return cumulative_distribution


# can be O(n) instead of O(log(n)) using Alias Method (https://www.keithschwarz.com/darts-dice-coins/)
# but it's ok for now :)
def weighted_selection_by_parameter(cumulative_distribution_list: List[float], selector_value: float = 0) -> int:
    if len(cumulative_distribution_list) == 0:
        raise Exception("cumulative_distribution_list should have at least 1 element!")
    left = 0
    right = len(cumulative_distribution_list)
    i = len(cumulative_distribution_list) // 2
    while not (i == 0 or (cumulative_distribution_list[i] >= selector_value > cumulative_distribution_list[i - 1])):
        if selector_value < cumulative_distribution_list[i]:
            right = i
            i = (left + i) // 2
        else:
            left = i
            i = (right + i) // 2
    return i


def weighted_random_selection(cumulative_distribution_list: List[float], seed: int = None) -> int:
    if len(cumulative_distribution_list) == 0:
        raise Exception("cumulative_distribution_list should have at least 1 element!")
    weight_summ = cumulative_distribution_list[-1]
    np.random.seed(seed)
    selector_value = np.random.rand() * weight_summ
    return weighted_selection_by_parameter(cumulative_distribution_list, selector_value)
