import functools
import time
from typing import List, Optional

from world_map_generator.default_values import DIAMOND_SQUARE_BASE_GRID_MAX_VALUE
from world_map_generator.generation import BiomeGenerator, FractalGenerator
from world_map_generator.generation.map_modifier import MapModifier
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import ValueChunk
from world_map_generator.rendering import save_biome_map_as_image, save_height_map_as_image
from world_map_generator.utils import (get_position_seed, weighted_random_selection, get_cumulative_distribution_list,
                                       Bounding)


def remove_modifier(height: float, biome_parameters: dict, value_maps_values: List[float] = None) -> float:
    threshold = 0.35 * DIAMOND_SQUARE_BASE_GRID_MAX_VALUE
    if height < threshold:
        return height
    else:
        drop = 1.0
        if value_maps_values is not None:
            drop = value_maps_values[0]
        # return height
        # return 1.15 * height - 100 * drop + 50
        return 1.5 * height + 30 - 100 * drop


def add_modifier(height: float, biome_parameters: dict, value_maps_values: List[float] = None) -> float:
    threshold = 0.75 * DIAMOND_SQUARE_BASE_GRID_MAX_VALUE
    if height < threshold:
        return height
    else:
        drop = 1.0
        if value_maps_values is not None:
            drop = value_maps_values[0]
        return threshold + (height - threshold) * 1.5 + 50 * drop


def cliff_modifier(height: float, biome_parameters: dict, value_maps_values: List[float] = None) -> float:
    threshold = 0.68 * DIAMOND_SQUARE_BASE_GRID_MAX_VALUE
    scaled_shift_map = DIAMOND_SQUARE_BASE_GRID_MAX_VALUE * value_maps_values[0]
    if scaled_shift_map < threshold:
        return 0.6 * height
    else:
        drop = 10.0
        return threshold + drop + 0.45 * (scaled_shift_map - 0.35*threshold) + (height - 1.35 * threshold) * 0.45


biome_example_1 = BiomeType(title='biome 1',
                            biome_parameters={'appearance_weight': 500},
                            height_modification=remove_modifier)
biome_example_2 = BiomeType(title='biome 2',
                            biome_parameters={'appearance_weight': 60},
                            height_modification=add_modifier)
biome_example_3 = BiomeType(title='biome 3',
                            biome_parameters={'appearance_weight': 800},
                            height_modification=cliff_modifier)
biome_types_pool = [biome_example_1, biome_example_2, biome_example_3]
biomes_weights = [b.biome_parameters['appearance_weight'] for b in biome_types_pool]
biomes_cumulative_distribution = get_cumulative_distribution_list(biomes_weights)


@functools.lru_cache(maxsize=1000, typed=False)
def get_random_biome_example(biome_node_x: int, biome_node_y: int, seed: int) -> BiomeType:
    pos_seed = get_position_seed(biome_node_x, biome_node_y, seed + 69)
    biome_index = weighted_random_selection(biomes_cumulative_distribution, pos_seed)
    return biome_types_pool[biome_index]


if __name__ == '__main__':
    seed = 52

    biome_grid_step = 50

    # bounding = Bounding(0, 0, 16, 16)
    bounding = Bounding(0, 0, 8, 8)

    height_map = Map()
    # height_map = Map(seed)
    generator = FractalGenerator(height_map.seed)
    start = time.process_time()
    bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds', '(heightmap)')
    save_height_map_as_image(height_map, 'heightmap',
                             max_color_value=2 * DIAMOND_SQUARE_BASE_GRID_MAX_VALUE)

    shift_map = Map(height_map.seed + 1)
    shift_generator = FractalGenerator(shift_map.seed, base_grid_max_value=1)
    start = time.process_time()
    wider_bounding = Bounding(0, 0, 1, 0)
    wider_bounding.add_bounding(bounding)
    wider_bounding.for_each(lambda x, y: shift_map.set_chunk(shift_generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds', '(shift_map)')
    save_height_map_as_image(shift_map, 'shift_map',
                             max_color_value=2 * DIAMOND_SQUARE_BASE_GRID_MAX_VALUE)

    biome_map = Map(height_map.seed)
    biome_generator = BiomeGenerator(biome_map.seed,
                                     biome_grid_step=biome_grid_step,
                                     get_biome_type=get_random_biome_example)
    start = time.process_time()
    bounding.for_each(lambda x, y: biome_map.set_chunk(biome_generator.generate_chunk(x, y, [shift_map])))
    print(time.process_time() - start, 'seconds', '(biome map)')
    save_biome_map_as_image(biome_map, 'biomes_map')

    def modify_heightmap_chunk(x: int, y: int):
        modified_chunk_values = modifier.modify_heightmap_chunk(x, y,
                                                                height_map.get_chunk(x, y),
                                                                biome_map.get_chunk(x, y),
                                                                [shift_map.get_chunk(x, y)])
        height_map.set_chunk(ValueChunk(x, y, tiles=modified_chunk_values))

    modifier = MapModifier(biome_map.seed)
    start = time.process_time()
    bounding.for_each(modify_heightmap_chunk)
    print(time.process_time() - start, 'seconds', '(modified heightmap)')
    print(f'seed = {height_map.seed}')
    print(height_map.number_of_generated_chunks(), height_map.number_of_generated_tiles())
    save_height_map_as_image(height_map, 'modified_heightmap_vm',
                             max_color_value=2 * DIAMOND_SQUARE_BASE_GRID_MAX_VALUE)
