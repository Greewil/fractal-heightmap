import time

from world_map_generator.default_values import DIAMOND_SQUARE_BASE_GRID_MAX_VALUE
from world_map_generator.generation import FractalGenerator
from world_map_generator.map import Map
from world_map_generator.rendering import save_height_map_as_image
from world_map_generator.utils import Bounding

if __name__ == '__main__':
    chunk_width = 64
    base_grid_distance = 64

    height_map = Map(chunk_width=chunk_width)
    generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance)
    print(f'seed = {height_map.seed}')
    start = time.process_time()
    bounding = Bounding(0, 0, 8, 8)
    bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    # # Its equivalent of:
    # for i in range(0, 8):
    #     for j in range(0, 8):
    #         height_map.set_chunk(generator.generate_chunk(i, j))
    print(time.process_time() - start, 'seconds')
    print(height_map.number_of_generated_chunks(), height_map.number_of_generated_tiles())
    save_height_map_as_image(height_map, 'tst', max_color_value=1.5 * DIAMOND_SQUARE_BASE_GRID_MAX_VALUE)
