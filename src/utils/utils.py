import math
import random
import sys
from random import random as rand
from typing import List, Tuple

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


# TODO there is a much more efficient algorithm for this
def random_selector_from_param(list_with_weights: List, selector_value: float = 0):
    if (selector_value < 0) or (selector_value >= 1):
        rnd_val = 0
    else:
        rnd_val = selector_value
    summ = sum([x.weight for x in list_with_weights])
    if summ == 0:
        return list_with_weights[int(rnd_val * len(list_with_weights))]
    else:
        rnd = summ * rnd_val
        selected_element = None
        for x in list_with_weights:
            if rnd > summ - x.weight:
                selected_element = x
                break
            else:
                summ -= x.weight
        return selected_element


# TODO there is a much more efficient algorithm for this
def random_selector(list_with_weights: List, seed=0):
    if seed == 0:
        cur_seed = get_random_seed()
    else:
        cur_seed = seed
    return random_selector_from_param(list_with_weights, random_from_seed(cur_seed))


def get_double_list_bounding(double_list: List[List]) -> Bounding:
    if len(double_list) > 0:
        return Bounding(0, 0, len(double_list), len(double_list[0]))
    else:
        return Bounding(0, 0, 0, 0)
