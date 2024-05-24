from typing import List, Tuple

import numpy as np

from world_map_generator.generation import MapComposer
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import ValueChunk


def test_composing_chunk():
    chunk_width = 32
    tiles_1 = np.random.rand(chunk_width * chunk_width).reshape((chunk_width, chunk_width))
    chunk_1 = ValueChunk(1, 1, chunk_width, tiles_1)
    tiles_2 = np.random.rand(chunk_width * chunk_width).reshape((chunk_width, chunk_width))
    chunk_2 = ValueChunk(1, 1, chunk_width, tiles_2)

    def composing_func_1(seed: int, tile_x: int, tile_y: int, tiles: List[float | Tuple[float, BiomeType]]) -> float:
        return sum(tiles)

    map_composer_1 = MapComposer(chunk_width=chunk_width, composing_func=composing_func_1)
    composed_chunk_1 = map_composer_1.compose_chunks(1, 1, [chunk_1, chunk_2])
    for x in range(map_composer_1.chunk_width):
        for y in range(map_composer_1.chunk_width):
            cur_value = composing_func_1(map_composer_1.seed,
                                         chunk_width + x,
                                         chunk_width + y,
                                         [c.get_tile(x, y) for c in [chunk_1, chunk_2]])
            assert composed_chunk_1.get_tile(x, y) == cur_value

    def composing_func_2(seed: int, tile_x: int, tile_y: int, tiles: List[float | Tuple[float, BiomeType]]) -> float:
        return sum(tiles) + seed * (tile_x + tile_y)

    map_composer_2 = MapComposer(chunk_width=chunk_width, composing_func=composing_func_2)
    composed_chunk_2 = map_composer_2.compose_chunks(1, 1, [chunk_1, chunk_2])
    for x in range(map_composer_2.chunk_width):
        for y in range(map_composer_2.chunk_width):
            cur_value = composing_func_2(map_composer_2.seed,
                                         chunk_width + x,
                                         chunk_width + y,
                                         [c.get_tile(x, y) for c in [chunk_1, chunk_2]])
            assert composed_chunk_2.get_tile(x, y) == cur_value
