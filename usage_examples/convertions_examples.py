import time

from world_map_generator.generation import FractalGenerator
from world_map_generator.map import Map
from world_map_generator.utils import Bounding
from world_map_generator.utils.convertors import json_to_value_chunk, value_chunk_to_json, map_region_to_json

if __name__ == '__main__':
    chunk_width = 64
    base_grid_distance = 64

    height_map = Map(chunk_width=chunk_width)
    generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance)
    print(f'seed = {height_map.seed}')
    start = time.process_time()
    bounding = Bounding(0, 0, 8, 8)
    bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')
    print(height_map.number_of_generated_chunks(), height_map.number_of_generated_tiles())

    value_chunk_json_str = value_chunk_to_json(height_map.get_chunk(1, 1))
    chunk_value = json_to_value_chunk(value_chunk_json_str)
    with open('chunk.json', 'w') as file:
        file.write(value_chunk_json_str)
    with open('map_region.json', 'w') as file:
        bounding = Bounding(-1, -1, 9, 9)
        file.write(map_region_to_json(height_map, bounding))
