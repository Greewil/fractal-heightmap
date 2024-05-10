import time

from world_map_generator.generation import FractalGenerator, DistortionGenerator
from world_map_generator.map import Map
from world_map_generator.rendering import save_height_map_as_image
from world_map_generator.utils import Bounding


if __name__ == '__main__':
    chunk_width = 64
    base_grid_distance = 64

    # seed = 4235214894
    seed = None

    start = time.process_time()
    bounding = Bounding(-1, -1, 9, 9)
    height_map = Map(seed=seed, chunk_width=chunk_width)
    seed = height_map.seed
    print(f'seed = {seed}')
    generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance, 1)
    bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')

    start = time.process_time()
    bounding = Bounding(0, 0, 8, 8)
    distortion_x_map = Map(seed=seed + 41, chunk_width=chunk_width)
    distortion_x_generator = FractalGenerator(distortion_x_map.seed, chunk_width, base_grid_distance, 1)
    bounding.for_each(lambda x, y: distortion_x_map.set_chunk(distortion_x_generator.generate_chunk(x, y)))
    distortion_y_map = Map(seed=seed + 42, chunk_width=chunk_width)
    distortion_y_generator = FractalGenerator(distortion_y_map.seed, chunk_width, base_grid_distance, 1)
    bounding.for_each(lambda x, y: distortion_y_map.set_chunk(distortion_y_generator.generate_chunk(x, y)))
    print(time.process_time() - start, 'seconds')

    start = time.process_time()
    height_map_distorted = Map(height_map.seed + 2, chunk_width=chunk_width)
    distortion_generator = DistortionGenerator(chunk_width)
    bounding = Bounding(0, 0, 8, 8)
    bounding.for_each(lambda x, y: height_map_distorted.set_chunk(
        distortion_generator.distort_map_chunk(x, y, height_map,
                                               distortion_x_map.get_chunk(x, y),
                                               distortion_y_map.get_chunk(x, y))))
    print(time.process_time() - start, 'seconds')
    save_height_map_as_image(height_map_distorted, 'height_map_distorted', max_color_value=1)
