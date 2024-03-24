import functools
import time

from world_map_generator.generation import BiomeGenerator, FractalGenerator
from world_map_generator.generation.map_modifier import MapModifier
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import ValueChunk
from world_map_generator.rendering import save_biome_map_as_image, save_height_map_as_image
from world_map_generator.utils import (get_position_seed, weighted_random_selection, get_cumulative_distribution_list,
                                       Bounding)


def cliff_modifier(height: float, biome_parameters: dict) -> float:
    if height < 50:
        return height
    else:
        drop = 40.0
        return (height + drop) * 100 / (drop + 100)


def multiply_modifier(height: float, biome_parameters: dict) -> float:
    threshold = 50
    if height < threshold:
        return height
    else:
        return threshold + (height - threshold) * 1.5


def volcano_modifier(height: float, biome_parameters: dict) -> float:
    height = multiply_modifier(height, biome_parameters)
    threshold = 105
    if height < threshold:
        return height
    else:
        return threshold - 1.7 * (height - threshold)


biome_example_1 = BiomeType(title='biome 1',
                            biome_parameters={'appearance_weight': 2},
                            height_modification=cliff_modifier)
biome_example_2 = BiomeType(title='biome 2',
                            biome_parameters={'appearance_weight': 0.5},
                            height_modification=multiply_modifier)
biome_example_3 = BiomeType(title='biome 3',
                            biome_parameters={'appearance_weight': 0.2},
                            height_modification=volcano_modifier)
biome_types_pool = [biome_example_1, biome_example_2, biome_example_3]
biomes_weights = [b.biome_parameters['appearance_weight'] for b in biome_types_pool]
biomes_cumulative_distribution = get_cumulative_distribution_list(biomes_weights)


@functools.lru_cache(maxsize=1000, typed=False)
def get_random_biome_example(biome_node_x: int, biome_node_y: int, seed: int) -> BiomeType:
    pos_seed = get_position_seed(biome_node_x, biome_node_y, seed + 69)
    biome_index = weighted_random_selection(biomes_cumulative_distribution, pos_seed)
    return biome_types_pool[biome_index]


if __name__ == '__main__':

    chunk_width = 64

    # base_grid_distance = 64
    base_grid_distance = chunk_width
    base_grid_max_value = 100

    biome_grid_step = 100
    biome_blend_radios = 10

    seed = 52

    # bounding = Bounding(0, 0, 16, 16)
    bounding = Bounding(0, 0, 8, 8)

    height_map = Map(seed, chunk_width=chunk_width)
    generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance, base_grid_max_value)
    start = time.process_time()
    for i in range(bounding.left, bounding.right):
        for j in range(bounding.bottom, bounding.top):
            height_map.set_chunk(ValueChunk(i, j, tiles=generator.generate_chunk_of_values(i, j)))
    print(time.process_time() - start, 'seconds', '(heightmap)')
    save_height_map_as_image(height_map, 'heightmap', max_color_value=1.5 * base_grid_max_value)

    shift_map = Map(seed + 1, chunk_width=chunk_width)
    shift_generator = FractalGenerator(shift_map.seed, chunk_width, base_grid_distance, 1)
    start = time.process_time()
    for i in range(bounding.left, bounding.right + 1):
        for j in range(bounding.bottom, bounding.top):
            shift_map.set_chunk(ValueChunk(i, j, tiles=shift_generator.generate_chunk_of_values(i, j)))
    print(time.process_time() - start, 'seconds', '(shift_map)')
    save_height_map_as_image(shift_map, 'shift_map', max_color_value=1.5 * base_grid_max_value)

    biome_map = Map(seed, chunk_width=chunk_width)
    generator = BiomeGenerator(biome_map.seed, chunk_width, biome_grid_step, biome_blend_radios)
    start = time.process_time()
    for i in range(bounding.left, bounding.right):
        for j in range(bounding.bottom, bounding.top):
            closest_biomes = generator.get_closes_biomes(i, j, get_random_biome_example)
            print(i, j, len(closest_biomes), 'closest_biomes')
            # chunk = generator.generate_chunk_of_values(i, j, closest_biomes)
            chunk = generator.generate_chunk_of_values_fast_voronoi(i, j, closest_biomes, [shift_map])
            biome_map.set_chunk(chunk)
    print(time.process_time() - start, 'seconds', '(biome map)')
    save_biome_map_as_image(biome_map, 'biomes_map')

    modifier = MapModifier(biome_map.seed, chunk_width)
    start = time.process_time()
    for i in range(bounding.left, bounding.right):
        for j in range(bounding.bottom, bounding.top):
            modified_chunk_values = modifier.modify_heightmap_chunk(i, j,
                                                                    height_map.get_chunk(i, j),
                                                                    biome_map.get_chunk(i, j))
            height_map.set_chunk(ValueChunk(i, j, tiles=modified_chunk_values))
    print(time.process_time() - start, 'seconds', '(modified heightmap)')
    print(f'seed = {height_map.seed}')
    print(height_map.number_of_generated_chunks(), height_map.number_of_generated_tiles())
    save_height_map_as_image(height_map, 'modified_heightmap', max_color_value=1.5 * base_grid_max_value)
