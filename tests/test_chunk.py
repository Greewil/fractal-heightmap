import numpy as np
import pytest
from numpy.testing import assert_array_equal

from world_map_generator.map.chunk import ValueChunk, chunk_dict_to_chunk, BiomeChunk, json_to_chunk


@pytest.mark.parametrize("test_input", [
    1.1, 0.0, -5.1,
])
def test_get_set_tile_value_chunk(test_input):
    chunk = ValueChunk(1, 14)
    chunk.set_tile(0, 0, test_input)
    assert test_input == chunk.get_tile(0, 0)


@pytest.mark.skip(reason="TODO")
@pytest.mark.parametrize("test_input", [
    [(1.1)], [(0.0)], [(-5.1)],
])
def test_get_set_tile_biome_chunk(test_input):
    # TODO
    chunk = ValueChunk(1, 14)
    chunk.set_tile(0, 0, test_input)
    assert test_input == chunk.get_tile(0, 0)


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
    assert value_chunk.chunk_type == 'ValueChunk'
    assert biome_chunk.chunk_type == 'BiomeChunk'


def test_convert_value_chunk_to_dict():
    chunk_width = 32
    tiles = np.random.rand(chunk_width * chunk_width).reshape((chunk_width, chunk_width))
    chunk = ValueChunk(1, 14, chunk_width, tiles)
    chunk_as_dict = chunk.to_dict()
    assert chunk_dict_to_chunk(chunk_as_dict).chunk_width == chunk_width
    assert chunk_dict_to_chunk(chunk_as_dict).chunk_type == chunk.chunk_type
    assert chunk_dict_to_chunk(chunk_as_dict).position == chunk.position
    assert_array_equal(chunk_dict_to_chunk(chunk_as_dict).tiles, chunk.tiles)


@pytest.mark.skip(reason="TODO")
def test_convert_biome_chunk_to_dict():
    assert True is True


def test_convert_value_chunk_to_json():
    chunk_width = 32
    tiles = np.random.rand(chunk_width * chunk_width).reshape((chunk_width, chunk_width))
    chunk = ValueChunk(1, 14, chunk_width, tiles)
    chunk_as_json = chunk.to_json()
    assert json_to_chunk(chunk_as_json).chunk_width == chunk_width
    assert json_to_chunk(chunk_as_json).chunk_type == chunk.chunk_type
    assert json_to_chunk(chunk_as_json).position == chunk.position
    assert_array_equal(json_to_chunk(chunk_as_json).tiles, chunk.tiles)


@pytest.mark.skip(reason="TODO")
def test_convert_biome_chunk_to_json():
    assert True is True
