import math

from .fixtures.chunks import chunk_width, tiles_for_value_chunk  # noqa: F401
from .fixtures.maps import map_bounding, random_value_map  # noqa: F401

from world_map_generator.generation import DistortionGenerator
from world_map_generator.map.chunk import ValueChunk


def test_composing_chunk(chunk_width, tiles_for_value_chunk, map_bounding, random_value_map):
    shift_chunk = ValueChunk(0, 0, chunk_width, tiles_for_value_chunk)
    initial_map = random_value_map

    distorter_zero_amplitude = DistortionGenerator(chunk_width, 0)
    distorted_chunk = distorter_zero_amplitude.distort_map_chunk(0, 0, initial_map, shift_chunk, shift_chunk)
    for x in range(chunk_width):
        for y in range(chunk_width):
            assert distorted_chunk.get_tile(x, y) == initial_map.get_tile(x, y)

    distortion_generator = DistortionGenerator(chunk_width, chunk_width)
    distorted_chunk = distortion_generator.distort_map_chunk(0, 0, initial_map, shift_chunk, shift_chunk)
    for x in range(chunk_width):
        for y in range(chunk_width):
            new_x = math.floor(x + chunk_width * (2 * shift_chunk.get_tile(x, y) - 1))
            new_y = math.floor(y + chunk_width * (2 * shift_chunk.get_tile(x, y) - 1))
            assert distorted_chunk.get_tile(x, y) == initial_map.get_tile(new_x, new_y)
