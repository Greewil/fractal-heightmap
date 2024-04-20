import time

from world_map_generator.generation import FractalGenerator
from world_map_generator.map import Map
from world_map_generator.rendering import save_height_map_as_image

if __name__ == '__main__':
    chunk_width = 64
    base_grid_distance = 64

    height_map = Map(chunk_width=chunk_width)
    generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance)
    print(f'seed = {height_map.seed}')
    start = time.process_time()
    for i in range(-5, 6):
        for j in range(-1, 10):
            height_map.set_chunk(generator.generate_chunk(i, j))
    # # Or you can use bounding:
    # bounding = Bounding(-5, -1, 6, 10)
    # bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')
    print(height_map.number_of_generated_chunks(), height_map.number_of_generated_tiles())
    save_height_map_as_image(height_map, 'tst', max_color_value=150)
