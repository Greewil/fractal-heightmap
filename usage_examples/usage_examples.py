import time

from src.default_values import TILES_IN_CHUNK
from src.generation import FractalGenerator
from src.map import Map
from src.map.chunk import ValueChunk
from src.rendering import save_height_map_as_image
from src.utils import get_position_seed

if __name__ == '__main__':
    # chunk_width = 4
    # base_grid_distance = 16
    #
    # height_map = Map(42, 64)

    # chunk_width = 64
    # base_grid_distance = 64
    #
    # height_map = Map(4, 256)

    # start = time.process_time()
    # r = 1000
    # matrix = []
    # for i in range(r):
    #     matrix.append([])
    #     for j in range(r):
    #         v = get_position_seed(i, j, 0)
    #         # v = 1
    #         # matrix[i].append(v)
    #         # height_map.set_tile(i, j, get_position_seed(i, j, v))
    #         # print(v)
    # print(time.process_time()-start)
    # save_height_map_as_image(height_map, 'tst', max_color_value=8*r*r)

    # generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance)
    # # chunk = ValueChunk(0, 0, tiles=generator.generate_chunk_of_values(0, 0))
    # # print(chunk.tiles)
    # chunk = ValueChunk(0, 0, tiles=generator.generate_chunk_of_values(1, 1))
    # # print(chunk.tiles)
    # height_map.set_chunk(chunk)
    # save_height_map_as_image(height_map, 'tst', max_color_value=150)

    chunk_width = 64
    base_grid_distance = 64

    height_map = Map(chunk_width=chunk_width)
    generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance)
    print(f'seed = {height_map.seed}')
    start = time.process_time()
    # for i in range(-5, 2):
    #     for j in range(1, 6):
    for i in range(-5, 6):
        for j in range(-1, 10):
            # print(i, j)
            chunk = ValueChunk(i, j, tiles=generator.generate_chunk_of_values(i, j))
            height_map.set_chunk(chunk)
    print(time.process_time() - start, 'seconds')
    print(height_map.number_of_generated_chunks(), height_map.number_of_generated_tiles())
    save_height_map_as_image(height_map, 'tst', max_color_value=150)
