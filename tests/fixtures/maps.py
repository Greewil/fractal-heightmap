import pytest

from .chunks import generate_random_value_chunk_tiles, generate_random_biome_chunk_tiles, biome_types, \
    chunk_width  # noqa: F401
from world_map_generator.map import Map
from world_map_generator.map.chunk import ValueChunk, BiomeChunk
from world_map_generator.utils import Bounding


@pytest.fixture
def map_bounding():
    return Bounding(-3, -3, 5, 5)


@pytest.fixture
def random_value_map(chunk_width, map_bounding):
    initial_map = Map(chunk_width=chunk_width)

    def add_chunk_to_map(chunk_x, chunk_y):
        tiles = generate_random_value_chunk_tiles(chunk_width)
        chunk = ValueChunk(chunk_x, chunk_y, chunk_width, tiles)
        initial_map.set_chunk(chunk)

    map_bounding.for_each(lambda x, y: add_chunk_to_map(x, y))
    return initial_map


@pytest.fixture
def random_biome_map(chunk_width, biome_types, map_bounding):
    initial_map = Map(chunk_width=chunk_width)

    def add_chunk_to_map(chunk_x, chunk_y):
        tiles = generate_random_biome_chunk_tiles(chunk_width, biome_types)
        chunk = BiomeChunk(chunk_x, chunk_y, chunk_width, tiles)
        initial_map.set_chunk(chunk)

    map_bounding.for_each(lambda x, y: add_chunk_to_map(x, y))
    return initial_map
