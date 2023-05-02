import time

from new_src.default_values import TILES_IN_CHUNK
from new_src.generation import FractalGenerator
from new_src.map import Map, Chunk
from new_src.rendering import save_map_as_image
from new_src.utils import get_position_seed

if __name__ == '__main__':
    # chunk_width = 4
    # base_grid_distance = 4
    chunk_width = 64
    base_grid_distance = 64

    height_map = Map(42, chunk_width)
    # chunk = [[50]*TILES_IN_CHUNK for i in range(height_map.chunk_width)]
    # chunk = Chunk(0, 0, height_map.chunk_width, chunk)
    # height_map.set_chunk(chunk)
    # chunk = [[100]*TILES_IN_CHUNK for i in range(height_map.chunk_width)]
    # chunk = Chunk(3, 3, height_map.chunk_width, chunk)
    # height_map.set_chunk(chunk)
    # height_map.set_tile(-3, -16, 200)
    # height_map.delete_chunk(3, 3)
    # print(height_map, height_map.number_of_generated_tiles())
    # # TODO generate
    # save_map_as_image(height_map, 'tst.png')

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
    # save_map_as_image(height_map, 'tst', max_value=8*r*r)

    generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance)
    # chunk = Chunk(0, 0, tiles=generator.generate_chunk_of_values(0, 0))
    # print(chunk.tiles)
    # chunk = Chunk(0, 0, tiles=generator.generate_chunk_of_values(1, 1))
    # print(chunk.tiles)

    # chunk = Chunk(0, 0, tiles=generator.generate_chunk_of_values(0, 0))
    # height_map.set_chunk(chunk)
    start = time.process_time()
    for i in range(-5, 6):
        for j in range(1, 3):
            chunk = Chunk(i, j, tiles=generator.generate_chunk_of_values(i, j))
            height_map.set_chunk(chunk)
    print(time.process_time() - start)
    save_map_as_image(height_map, 'tst', max_value=150)

    # print(-1 % 2)
