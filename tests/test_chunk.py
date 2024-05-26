from .fixtures.chunks import *

import pytest
from numpy.testing import assert_array_equal

from world_map_generator.map.biome import BiomeType, are_biome_tiles_same
from world_map_generator.map.chunk import ValueChunk, chunk_dict_to_chunk, BiomeChunk, json_to_chunk


@pytest.mark.parametrize("tile_input", [
    1.1, 0.0, -5.1,
])
def test_get_set_tile_value_chunk(tile_input):
    chunk = ValueChunk(1, 14)
    chunk.set_tile(0, 0, tile_input)
    assert tile_input == chunk.get_tile(0, 0)


@pytest.mark.parametrize("tile_input", [
    [(1.1, BiomeType("biome 1"))], [(1.1, BiomeType("b1")), (3, BiomeType("b2"))],
])
def test_get_set_tile_biome_chunk(tile_input):
    chunk = BiomeChunk(1, 14)
    chunk.set_tile(0, 0, tile_input)
    for n, weighted_biome in enumerate(tile_input):
        assert weighted_biome[0] == chunk.get_tile(0, 0)[n][0]
        assert weighted_biome[1].title == chunk.get_tile(0, 0)[n][1].title


def test_copy_value_chunk():
    chunk1 = ValueChunk(1, 14, 64)
    chunk2 = ValueChunk(1, 14, chunk1.chunk_width, chunk1.tiles)
    for x in range(chunk1.chunk_width):
        for y in range(chunk1.chunk_width):
            assert chunk1.get_tile(x, y) == chunk2.get_tile(x, y)


def test_copy_biome_chunk():
    chunk1 = BiomeChunk(1, 14, 64)
    chunk2 = BiomeChunk(1, 14, chunk1.chunk_width, chunk1.tiles)
    for x in range(chunk1.chunk_width):
        for y in range(chunk1.chunk_width):
            assert chunk1.get_tile(x, y) == chunk2.get_tile(x, y)


def test_invalid_copy_value_chunk():
    with pytest.raises(Exception):
        chunk1 = ValueChunk(1, 14, 64)
        ValueChunk(1, 14, 128, chunk1.tiles)


def test_invalid_copy_biome_chunk():
    with pytest.raises(Exception):
        chunk1 = BiomeChunk(1, 14, 64)
        BiomeChunk(1, 14, 128, chunk1.tiles)


def test_get_chunk_type():
    value_chunk = ValueChunk(1, 1)
    biome_chunk = BiomeChunk(1, 1)
    assert value_chunk.chunk_type == "ValueChunk"
    assert biome_chunk.chunk_type == "BiomeChunk"


def test_convert_value_chunk_to_dict(chunk_width, tiles_for_value_chunk):
    chunk = ValueChunk(1, 14, chunk_width, tiles_for_value_chunk)
    chunk_as_dict = chunk.to_dict()
    chunk_from_dict = chunk_dict_to_chunk(chunk_as_dict)
    assert chunk_from_dict.chunk_width == chunk_width
    assert chunk_from_dict.chunk_type == chunk.chunk_type
    assert chunk_from_dict.position == chunk.position
    assert_array_equal(chunk_from_dict.tiles, chunk.tiles)


def test_convert_value_chunk_to_json(chunk_width, tiles_for_value_chunk):
    chunk = ValueChunk(1, 14, chunk_width, tiles_for_value_chunk)
    chunk_as_json = chunk.to_json()
    chunk_from_json = json_to_chunk(chunk_as_json)
    assert chunk_from_json.chunk_width == chunk_width
    assert chunk_from_json.chunk_type == chunk.chunk_type
    assert chunk_from_json.position == chunk.position
    assert_array_equal(chunk_from_json.tiles, chunk.tiles)


def test_convert_biome_chunk_to_dict(chunk_width, biome_types, tiles_for_biome_chunk):
    chunk = BiomeChunk(1, 14, chunk_width, tiles_for_biome_chunk)
    chunk_as_dict = chunk.to_dict()
    chunk_from_dict = chunk_dict_to_chunk(chunk_as_dict, biome_types)
    assert chunk_from_dict.chunk_width == chunk_width
    assert chunk_from_dict.chunk_type == chunk.chunk_type
    assert chunk_from_dict.position == chunk.position
    for x in range(chunk_width):
        for y in range(chunk_width):
            assert are_biome_tiles_same(chunk_from_dict.get_tile(x, y), chunk.get_tile(x, y)) is True


def test_convert_biome_chunk_to_json(chunk_width, biome_types, tiles_for_biome_chunk):
    chunk = BiomeChunk(1, 14, chunk_width, tiles_for_biome_chunk)
    chunk_as_json = chunk.to_json()
    chunk_from_json = json_to_chunk(chunk_as_json, biome_types)
    assert chunk_from_json.chunk_width == chunk_width
    assert chunk_from_json.chunk_type == chunk.chunk_type
    assert chunk_from_json.position == chunk.position
    for x in range(chunk_width):
        for y in range(chunk_width):
            assert are_biome_tiles_same(chunk_from_json.get_tile(x, y), chunk.get_tile(x, y)) is True
