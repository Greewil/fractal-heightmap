import time
from copy import deepcopy
from typing import Optional

import numpy as np

from world_map_generator.default_values import DIAMOND_SQUARE_BASE_GRID_MAX_VALUE
from world_map_generator.generation import FractalGenerator
from world_map_generator.generation.primitives.round_structure import RoundStructureType, \
    COS_COS_ROUND_STRUCTURE_TYPE, COS_HYPERBOLE_ROUND_STRUCTURE_TYPE, COS_ROUND_STRUCTURE_TYPE, \
    LINEAR_ROUND_STRUCTURE_TYPE, STEP_ROUND_STRUCTURE_TYPE
from world_map_generator.generation.round_structures_generator import DotsGenerator, get_value_intersection_max, \
    get_value_intersection_sum_clip
from world_map_generator.map import Map
from world_map_generator.rendering import save_height_map_as_image
from world_map_generator.utils import Bounding, get_position_seed


def cos_cos_cos_radius_function(r: float, max_r: float, dx: float, dy: float, max_value: float,
                                parameters: Optional[dict] = None) -> float:
    cur_rotation = np.arctan2(dx, dy) + parameters['rotation']
    cos_r = 3 * 0.5 * (1 + np.cos(r * np.pi / max_r))
    return np.cos(3 * cur_rotation) * max_value * 0.5 * (1 + np.cos(np.pi * (1 - cos_r)))


COS_COS_COS_ROUND_STRUCTURE_TYPE = RoundStructureType('Cos(cos)*cos(a) round structure',
                                                      radius_function=cos_cos_cos_radius_function)


if __name__ == '__main__':
    chunk_width = 64
    base_grid_distance = 64

    # seed = 4235214894
    seed = 2258822325
    # seed = None

    height_map = Map(seed=seed, chunk_width=chunk_width)
    print(f'seed = {height_map.seed}')
    # generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance)
    # start = time.process_time()
    # bounding = Bounding(0, 0, 8, 8)
    # bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    # print(time.process_time() - start, 'seconds')

    def get_round_structure_type(seed: int,
                                 round_structure_node_x: int, round_structure_node_y: int,
                                 tile_x: int, tile_y: int) -> RoundStructureType | None:
        pos_seed = get_position_seed(round_structure_node_x, round_structure_node_y, seed)
        np.random.seed(pos_seed)
        rnd = np.random.rand(4)

        # round_structure_cos_cos = deepcopy(COS_ROUND_STRUCTURE_TYPE)
        # round_structure_cos_cos = deepcopy(COS_COS_ROUND_STRUCTURE_TYPE)
        round_structure_cos_cos = deepcopy(COS_COS_COS_ROUND_STRUCTURE_TYPE)
        # round_structure_cos_cos = deepcopy(STEP_ROUND_STRUCTURE_TYPE)
        round_structure_cos_cos.parameters['rotation'] = rnd[3] * 2 * np.pi
        round_structure_cos_cos.max_r = 25 + 85 * rnd[1]
        round_structure_cos_cos.max_value = 0.25 + 0.75 * rnd[2]
        # round_structure_cos_hyperbole = deepcopy(STEP_ROUND_STRUCTURE_TYPE)
        # round_structure_cos_hyperbole = deepcopy(LINEAR_ROUND_STRUCTURE_TYPE)
        # round_structure_cos_hyperbole = deepcopy(COS_ROUND_STRUCTURE_TYPE)
        round_structure_cos_hyperbole = deepcopy(COS_HYPERBOLE_ROUND_STRUCTURE_TYPE)
        round_structure_cos_hyperbole.max_r = 25 + 50 * rnd[1]
        if rnd[0] > 0.5 * tile_x * 0.0035:
            return round_structure_cos_cos
        elif rnd[0] > 0.3:
            return round_structure_cos_hyperbole
        else:
            return None

    round_structures_map = Map(height_map.seed, chunk_width=chunk_width)
    generator = DotsGenerator(round_structures_map.seed, chunk_width, 100,
                              get_round_structure_type, get_value_intersection_sum_clip)
    start = time.process_time()
    bounding = Bounding(0, 0, 8, 8)
    bounding.for_each(lambda x, y: round_structures_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')
    print(round_structures_map.number_of_generated_chunks(), round_structures_map.number_of_generated_tiles())
    save_height_map_as_image(round_structures_map, 'round_structures1', max_color_value=1)
