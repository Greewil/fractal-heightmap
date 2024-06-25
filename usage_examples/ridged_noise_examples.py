import time
from math import floor
from typing import Tuple, List, Callable

from world_map_generator.generation import FractalGenerator, MapComposer, DistortionGenerator
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.rendering import save_height_map_as_image
from world_map_generator.utils import Bounding


def generate_base_height_map(seed: int | None, chunk_width: int, bounding: Bounding) -> Map:
    start = time.process_time()
    output_map = Map(seed, chunk_width)
    print(f'height map (seed={output_map.seed})')
    generator = FractalGenerator(output_map.seed, base_grid_max_value=1.0)
    bounding.for_each(lambda x, y: output_map.set_chunk(generator.generate_chunk(x, y)))
    print(f'{time.process_time() - start:.3f}', 'seconds')
    return output_map


def compose_two_maps(composer_seed: int | None, chunk_width: int, bounding: Bounding, composing_method: Callable,
                     map_1: Map, map_2: Map) -> Map:
    start = time.process_time()
    output_map = Map(composer_seed, chunk_width)
    print(f'composing map (seed={output_map.seed})')
    map_composer = MapComposer(output_map.seed + 1, chunk_width, composing_method)
    bounding.for_each(lambda x, y: output_map.set_chunk(
        map_composer.compose_chunks(x, y, [map_1.get_chunk(x, y), map_2.get_chunk(x, y)])))
    print(f'{time.process_time() - start:.3f}', 'seconds')
    return output_map


def distort_map(composer_seed: int | None, chunk_width: int, bounding: Bounding,
                map_to_distort: Map, shift_map: Map) -> Map:
    start = time.process_time()
    output_map = Map(composer_seed, chunk_width)
    print(f'distorting map (seed={output_map.seed})')
    distortion_generator = DistortionGenerator(chunk_width, floor(0.5 * chunk_width))
    bounding.for_each(lambda x, y: output_map.set_chunk(
        distortion_generator.distort_map_chunk(x, y, map_to_distort,
                                               shift_map.get_chunk(x, y),
                                               shift_map.get_chunk(x + 1, y + 1))))
    print(f'{time.process_time() - start:.3f}', 'seconds')
    return output_map


if __name__ == '__main__':
    chunk_width = 64
    base_grid_distance = 64

    # seed = 4235214894
    seed = None
    bounding = Bounding(0, 0, 8, 8)
    wider_bounding = bounding.get_wider_bounding(1)

    height_map_1 = generate_base_height_map(seed, chunk_width, wider_bounding)
    height_map_2 = generate_base_height_map(height_map_1.seed + 1, chunk_width, wider_bounding)

    distorted_map_1 = distort_map(height_map_2.seed + 1, chunk_width, bounding, height_map_1, height_map_2)

    def composing_func(seed: int, tile_x: int, tile_y: int, tiles: List[float | Tuple[float, BiomeType]]) -> float:
        def module(value: float, clip_level: float) -> float:
            if value > clip_level:
                return value
            else:
                return 2 * clip_level - value

        # return 0.5 * (tiles[0] + module(tiles[1], 0.5))
        return 1 + 0.5 * tiles[0] - module(tiles[1], 0.5)
        # return 1 + 0.5 * tiles[1] - module(tiles[0], 0.5)
        # return 1.5 * tiles[1] - 0.5 * module(tiles[0], 0.5)
        # return 0.5 * tiles[0] + 0.5 * module(tiles[1], 0.25 + 0.55 * sin(0.03 * tile_x) * sin(0.03 * tile_y))

    ridged_map = compose_two_maps(height_map_2.seed + 1, chunk_width, bounding, composing_func,
                                  height_map_2, distorted_map_1)

    save_height_map_as_image(ridged_map, 'ridged_heightmap', max_color_value=1.5)
