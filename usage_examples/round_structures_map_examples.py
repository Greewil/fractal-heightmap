import time
from copy import deepcopy
from math import sin
from typing import Optional, Tuple, List

import numpy as np

from world_map_generator.default_values import DIAMOND_SQUARE_BASE_GRID_MAX_VALUE
from world_map_generator.generation import FractalGenerator, MapComposer, DistortionGenerator
from world_map_generator.generation.primitives.round_structure import RoundStructureType, \
    COS_COS_ROUND_STRUCTURE_TYPE, COS_HYPERBOLE_ROUND_STRUCTURE_TYPE, COS_ROUND_STRUCTURE_TYPE, \
    LINEAR_ROUND_STRUCTURE_TYPE, STEP_ROUND_STRUCTURE_TYPE
from world_map_generator.generation.round_structures_generator import DotsGenerator, get_value_intersection_max, \
    get_value_intersection_sum_clip, get_value_intersection_sum, get_d_xy_euclidean, get_d_xy_min, get_d_xy_l3, \
    get_d_xy_l4, get_d_xy_l3_abs, get_d_xy_l05, get_d_xy_max, get_d_xy_euclidean_cos, get_d_xy_sum
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import ValueChunk
from world_map_generator.rendering import save_height_map_as_image
from world_map_generator.utils import Bounding, get_position_seed


def cos_cos_cos_radius_function(r: float, max_r: float, dx: float, dy: float, max_value: float,
                                parameters: Optional[dict], filling_value: float) -> float:
    cur_rotation = np.arctan2(dx, dy) + parameters['rotation']
    cos_r = 3 * 0.5 * (1 + np.cos(r * np.pi / max_r))
    return np.cos(3 * cur_rotation) * max_value * 0.5 * (1 + np.cos(np.pi * (1 - cos_r)))


def atoll_radius_function(r: float, max_r: float, dx: float, dy: float, max_value: float,
                          parameters: Optional[dict], filling_value: float) -> float:
    relative_r = r / max_r
    # TODO add atoll line width, close clip, far clip
    if relative_r < 0.55:
        return filling_value
    else:
        cur_rotation = np.arctan2(dx, dy) + parameters.get('rotation', 0)
        r_modifier = max_value * 0.5 * (1 + np.cos(5 * (relative_r - 0.8) * np.pi))
        rotation_modifier = np.cos(cur_rotation)
        return max(0, rotation_modifier * r_modifier)


ATOLL_STRUCTURE_TYPE = RoundStructureType('Atoll', radius_function=atoll_radius_function)


if __name__ == '__main__':
    chunk_width = 64
    base_grid_distance = 64

    # seed = 4235214894
    seed = 668760324
    # seed = None

    start = time.process_time()
    height_map = Map(seed=seed, chunk_width=chunk_width)
    seed = height_map.seed
    print(f'seed = {seed}')
    generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance, 1)
    bounding = Bounding(0, 0, 8, 8)
    bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')

    def get_round_structure_type(seed: int,
                                 round_structure_node_x: int, round_structure_node_y: int,
                                 tile_x: int, tile_y: int) -> RoundStructureType | None:
        pos_seed = get_position_seed(round_structure_node_x, round_structure_node_y, seed)
        np.random.seed(pos_seed)
        rnd = np.random.rand(4)

        # round_structure_cos_cos = deepcopy(COS_ROUND_STRUCTURE_TYPE)
        # round_structure_cos_cos = deepcopy(COS_COS_ROUND_STRUCTURE_TYPE)
        round_structure_cos_cos = deepcopy(ATOLL_STRUCTURE_TYPE)
        # round_structure_cos_cos = deepcopy(STEP_ROUND_STRUCTURE_TYPE)
        round_structure_cos_cos.parameters['rotation'] = rnd[3] * 2 * np.pi
        round_structure_cos_cos.max_r = 25 + 85 * rnd[1]
        # round_structure_cos_cos.max_value = 0.25 + 0.75 * rnd[2]
        round_structure_cos_cos.max_value = 0.25 + 0.75 * rnd[2]
        # round_structure_cos_hyperbole = deepcopy(STEP_ROUND_STRUCTURE_TYPE)
        # round_structure_cos_hyperbole = deepcopy(LINEAR_ROUND_STRUCTURE_TYPE)
        # round_structure_cos_hyperbole = deepcopy(COS_ROUND_STRUCTURE_TYPE)
        round_structure_cos_hyperbole = deepcopy(COS_HYPERBOLE_ROUND_STRUCTURE_TYPE)
        round_structure_cos_hyperbole.max_r = 25 + 50 * rnd[1]
        round_structure_cos_hyperbole.max_value = 0.35 + 0.65 * rnd[2]
        if rnd[0] > 0.5 * tile_x * 0.0035:
            return round_structure_cos_cos
        elif rnd[0] > 0.3:
            return round_structure_cos_hyperbole
        else:
            return None

    start = time.process_time()
    round_structures_map = Map(height_map.seed + 1, chunk_width=chunk_width)
    generator = DotsGenerator(round_structures_map.seed, chunk_width, 100, 1, 0.0,
                              get_round_structure_type, get_value_intersection_sum_clip(), get_d_xy_sum)
                              # get_round_structure_type, get_value_intersection_sum_clip(), get_d_xy_euclidean_cos(8))
    bounding = Bounding(-2, -2, 10, 10)
    bounding.for_each(lambda x, y: round_structures_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')
    save_height_map_as_image(round_structures_map, 'round_structures1', max_color_value=2)

    start = time.process_time()
    bounding = Bounding(-1, -1, 9, 9)
    # bounding = Bounding(0, 0, 8, 8)
    distortion_x_map = Map(seed=seed + 41, chunk_width=chunk_width)
    distortion_x_generator = FractalGenerator(distortion_x_map.seed, chunk_width, base_grid_distance, 1)
    bounding.for_each(lambda x, y: distortion_x_map.set_chunk(distortion_x_generator.generate_chunk(x, y)))
    distortion_y_map = Map(seed=seed + 42, chunk_width=chunk_width)
    distortion_y_generator = FractalGenerator(distortion_y_map.seed, chunk_width, base_grid_distance, 1)
    bounding.for_each(lambda x, y: distortion_y_map.set_chunk(distortion_y_generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')

    start = time.process_time()
    round_structures_map_distorted = Map(height_map.seed + 2, chunk_width=chunk_width)
    distortion_generator = DistortionGenerator(chunk_width)
    bounding = Bounding(-1, -1, 9, 9)
    # bounding = Bounding(0, 0, 8, 8)
    bounding.for_each(lambda x, y: round_structures_map_distorted.set_chunk(
        distortion_generator.distort_map_chunk(x, y, round_structures_map,
                                               distortion_x_map.get_chunk(x, y),
                                               distortion_y_map.get_chunk(x, y))))
    print(time.process_time() - start, 'seconds')
    save_height_map_as_image(round_structures_map_distorted, 'round_structures1_distorted', bounding, max_color_value=2)

    start = time.process_time()
    bounding = Bounding(0, 0, 8, 8)
    round_structures_map_distorted_x2 = Map(height_map.seed + 2, chunk_width=chunk_width)
    bounding.for_each(lambda x, y: round_structures_map_distorted_x2.set_chunk(
        distortion_generator.distort_map_chunk(x, y, round_structures_map_distorted,
                                               distortion_y_map.get_chunk(x, y),
                                               distortion_x_map.get_chunk(x, y))))
    print(time.process_time() - start, 'seconds')
    save_height_map_as_image(round_structures_map_distorted_x2, 'round_structures1_distorted_x2', bounding,
                             max_color_value=2)

    def composing_func(seed: int, tile_x: int, tile_y: int, tiles: List[float | Tuple[float, BiomeType]]) -> float:
        # return tiles[0] * (0.5 + tiles[1])
        return tiles[0] + 0.5 * tiles[1]
        # return tiles[0] + tiles[1] * sin(0.01 * tile_x)

    start = time.process_time()
    composed_map = Map(height_map.seed + 3, chunk_width=chunk_width)
    map_composer = MapComposer(height_map.seed, chunk_width, composing_func)
    bounding.for_each(lambda x, y: composed_map.set_chunk(
        map_composer.compose_chunks(x, y, [height_map.get_chunk(x, y),
                                           round_structures_map_distorted_x2.get_chunk(x, y)])))
    print(time.process_time() - start, 'seconds')
    print(round_structures_map.number_of_generated_chunks(), round_structures_map.number_of_generated_tiles())
    save_height_map_as_image(composed_map, 'round_structures1_composed', max_color_value=1.5)

    # chunk1 = ValueChunk(1, 14, 64)
    # chunk2 = ValueChunk(1, 14, 128, chunk1.tiles)
