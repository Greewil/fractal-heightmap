import time

from world_map_generator.generation import FractalGenerator, BiomeGenerator
from world_map_generator.map import Map
from world_map_generator.rendering import save_height_map_as_image
from world_map_generator.utils import Bounding
from world_map_generator.utils.convertors import json_to_value_chunk, chunk_to_json, map_region_to_json


def generate_base_height_map(bounding: Bounding) -> Map:
    height_map = Map()
    print(f'height map seed = {height_map.seed}')
    generator = FractalGenerator(height_map.seed, base_grid_max_value=1.0)
    start = time.process_time()
    bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')
    return height_map


def generate_base_biome_map(bounding: Bounding) -> Map:
    biome_map = Map()
    print(f'biome map seed = {biome_map.seed}')
    generator = BiomeGenerator(biome_map.seed)
    start = time.process_time()
    bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')
    return biome_map


if __name__ == '__main__':
    generation_bounding = Bounding(0, 0, 8, 8)
    print(vars(generation_bounding))

    # generate maps to convert them
    height_map = generate_base_height_map(generation_bounding)
    biome_map = generate_base_biome_map(generation_bounding)

    # convert value chunk to json back and force
    value_chunk_json_str = chunk_to_json(height_map.get_chunk(1, 1))
    chunk_value = json_to_value_chunk(value_chunk_json_str)

    # convert map region to json back and force
    map_region_json_str = map_region_to_json(height_map)
    # if bounding is None it will be set as bounding = value_map.bounding_chunks()
    height_map_restored = json_to_value_chunk(map_region_json_str)

    # save jsons
    with open('chunk.json', 'w') as file:
        file.write(value_chunk_json_str)
    with open('chunk_array.json', 'w') as file:
        file.write(map_region_json_str)
    with open('map_region.json', 'w') as file:
        file.write(map_region_json_str)

    # save restored maps as images
    save_height_map_as_image(height_map_restored, 'height_map_restored_from_json', max_color_value=1.5)
    # save_height_map_as_image(biome_map_restored, 'height_map_restored_from_json', max_color_value=1.5)
