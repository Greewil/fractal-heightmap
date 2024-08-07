import time
from math import sin
from typing import Tuple, List

from world_map_generator.generation import FractalGenerator, MapComposer
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.rendering import save_height_map_as_image
from world_map_generator.utils import Bounding


if __name__ == '__main__':
    chunk_width = 64
    base_grid_distance = 64

    # seed = 4235214894
    seed = None
    bounding = Bounding(0, 0, 8, 8)

    start = time.process_time()
    height_map_1 = Map(seed=seed, chunk_width=chunk_width)
    print(f'seed = {seed}')
    generator = FractalGenerator(height_map_1.seed, chunk_width, base_grid_distance, 1)
    bounding.for_each(lambda x, y: height_map_1.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')

    start = time.process_time()
    height_map_2 = Map(seed=height_map_1.seed + 1, chunk_width=chunk_width)
    generator = FractalGenerator(height_map_2.seed, chunk_width, base_grid_distance, 1)
    bounding.for_each(lambda x, y: height_map_2.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')

    def composing_func(seed: int, tile_x: int, tile_y: int, tiles: List[float | Tuple[float, BiomeType]]) -> float:
        return tiles[0] + tiles[1] * sin(0.03 * tile_x)

    start = time.process_time()
    composed_map = Map(height_map_2.seed, chunk_width=chunk_width)
    map_composer = MapComposer(height_map_2.seed + 1, chunk_width, composing_func)
    bounding.for_each(lambda x, y: composed_map.set_chunk(
        map_composer.compose_chunks(x, y, [height_map_1.get_chunk(x, y), height_map_2.get_chunk(x, y)])))
    print(time.process_time() - start, 'seconds')
    print(composed_map.number_of_generated_chunks(), composed_map.number_of_generated_tiles())
    save_height_map_as_image(composed_map, 'composed_heightmaps', max_color_value=2)
