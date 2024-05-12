import time
from math import floor

import numpy as np

from world_map_generator.generation import FractalGenerator, BiomeGenerator
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import json_to_chunk
from world_map_generator.map.map import json_to_map
from world_map_generator.rendering import save_height_map_as_image, save_biome_map_as_image
from world_map_generator.utils import Bounding, get_position_seed


BIOME_EXAMPLES_COUNT = 6

biome_examples = [BiomeType(title=f'biome {i}') for i in range(BIOME_EXAMPLES_COUNT)]


def generate_base_height_map(bounding: Bounding) -> Map:
    height_map = Map()
    print(f'height map seed = {height_map.seed}')
    generator = FractalGenerator(height_map.seed, base_grid_max_value=1.0)
    start = time.process_time()
    bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')
    return height_map


def generate_base_biome_map(bounding: Bounding, shift_map: Map) -> Map:
    def get_random_biome_example(biome_node_x: int, biome_node_y: int, seed: int) -> BiomeType:
        pos_seed = get_position_seed(biome_node_x, biome_node_y, seed)
        np.random.seed(pos_seed)
        biome_index = floor(np.random.rand() * BIOME_EXAMPLES_COUNT)
        return biome_examples[biome_index]

    biome_map = Map()
    print(f'biome map seed = {biome_map.seed}')
    generator = BiomeGenerator(biome_map.seed, get_biome_type=get_random_biome_example)
    start = time.process_time()
    bounding.for_each(lambda x, y: biome_map.set_chunk(generator.generate_chunk(x, y, [shift_map])))
    print(time.process_time() - start, 'seconds')
    return biome_map


if __name__ == '__main__':
    generation_bounding = Bounding(0, 0, 9, 8)
    print(vars(generation_bounding))

    # generate maps to convert them
    height_map = generate_base_height_map(generation_bounding)
    generation_bounding = Bounding(0, 0, 8, 8)
    biome_map = generate_base_biome_map(generation_bounding, height_map)

    # convert value chunk to json back and force
    value_chunk_json_str = height_map.get_chunk(1, 1).to_json()
    value_chunk = json_to_chunk(value_chunk_json_str)

    # convert biome chunk to json back and force
    biome_chunk_json_str = biome_map.get_chunk(1, 1).to_json()
    # biome_chunk = json_to_chunk(biome_chunk_json_str)

    # convert value map region to json back and force
    value_map_as_matrix_json_str = height_map.to_json_as_one_tile_matrix()
    value_map_as_chunks_list_json_str = height_map.to_json()
    # if bounding is None it will be set as bounding = value_map.bounding_chunks()
    height_map_restored = json_to_map(value_map_as_chunks_list_json_str)

    # convert biome map region to json back and force
    biome_map_as_matrix_json_str = biome_map.to_json_as_one_tile_matrix()
    biome_map_as_chunks_list_json_str = biome_map.to_json()
    biome_map_restored = json_to_map(biome_map_as_chunks_list_json_str, biome_examples)

    # save jsons
    with open('value_chunk.json', 'w') as file:
        file.write(value_chunk_json_str)
    with open('biome_chunk.json', 'w') as file:
        file.write(biome_chunk_json_str)
    with open('value_map_as_chunk_list.json', 'w') as file:
        file.write(value_map_as_chunks_list_json_str)
    with open('value_map_as_matrix.json', 'w') as file:
        file.write(value_map_as_matrix_json_str)
    with open('biome_map_as_chunk_list.json', 'w') as file:
        file.write(biome_map_as_chunks_list_json_str)
    with open('biome_map_as_matrix.json', 'w') as file:
        file.write(biome_map_as_matrix_json_str)

    # save restored maps as images
    save_height_map_as_image(height_map_restored, 'height_map_restored_from_json', max_color_value=1.5)
    save_biome_map_as_image(biome_map, 'biome_map_restored_from_json')
    # save_biome_map_as_image(biome_map_restored, 'biome_map_restored_from_json')
