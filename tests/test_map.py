import numpy as np
import pytest

from world_map_generator.map import Map
from world_map_generator.map.chunk import ValueChunk, BiomeChunk
from world_map_generator.utils import Bounding


@pytest.mark.parametrize("chunk_position", [
    (1, 1), (1_000_000_000_000, 1_000_000_000_000), (-1, -10), (-1_000_000_000_000, -1_000_000_000_000)
])
def test_create_value_chunk(chunk_position):
    chunk_width = 32
    testing_map = Map(chunk_width=chunk_width)
    testing_map.create_chunk(chunk_position[0], chunk_position[1])
    assert testing_map.get_chunk(chunk_position[0], chunk_position[1]) is not None
    assert testing_map.get_chunk(chunk_position[0], chunk_position[1] + 1) is None
    assert testing_map.chunk_type == 'ValueChunk'

    testing_map.create_chunk(chunk_position[0] + 1, chunk_position[1])
    assert testing_map.get_chunk(chunk_position[0] + 1, chunk_position[1]) is not None
    assert testing_map.chunk_type == 'ValueChunk'


@pytest.mark.parametrize("chunk_position", [
    (1, 1), (1_000_000_000_000, 1_000_000_000_000), (-1, -10), (-1_000_000_000_000, -1_000_000_000_000)
])
def test_create_biome_chunk(chunk_position):
    chunk_width = 32
    testing_map = Map(chunk_width=chunk_width)
    testing_map.set_chunk(BiomeChunk(0, 0, chunk_width))  # to set chunk_type
    testing_map.create_chunk(chunk_position[0], chunk_position[1])
    assert testing_map.get_chunk(chunk_position[0], chunk_position[1]) is not None
    assert testing_map.get_chunk(chunk_position[0], chunk_position[1] + 1) is None
    assert testing_map.chunk_type == 'BiomeChunk'


@pytest.mark.parametrize("tiles_input", [
    1.1, 0.0, -5.1, 1.0e100
])
def test_set_get_value_tile(tiles_input):
    chunk_width = 32
    testing_map = Map(chunk_width=chunk_width)
    testing_map.set_tile(1, 1, tiles_input)
    assert testing_map.get_tile(1, 1) == tiles_input
    assert testing_map.get_tile(1, 2) == 0.0  # empty tile
    assert testing_map.get_tile(chunk_width, 1) is None  # tile in chunk that wasn't generated yet

    tiles = np.random.rand(chunk_width * chunk_width).reshape((chunk_width, chunk_width))
    chunk = ValueChunk(1, 1, chunk_width, tiles)
    testing_map.set_chunk(chunk)
    assert testing_map.get_tile(chunk_width + 1, chunk_width + 1) == tiles[1][1]
    testing_map.set_tile(chunk_width + 1, chunk_width + 1, tiles_input)
    assert testing_map.get_tile(chunk_width + 1, chunk_width + 1) == tiles_input


@pytest.mark.parametrize("tiles_input", [
    1.1, 0.0, -5.1, 1.0e100
])
def test_set_value_tile_updates_chunk_type(tiles_input):
    chunk_width = 32
    testing_map = Map(chunk_width=chunk_width)
    testing_map.set_tile(0, 0, tiles_input)
    # here set tile with float value should create new ValueChunk so chunk_type of the map now should be ValueChunk
    assert testing_map.get_chunk(0, 0).chunk_type == 'ValueChunk'
    assert testing_map.chunk_type == 'ValueChunk'
    with pytest.raises(Exception):
        biome_chunk = BiomeChunk(1, 14, chunk_width)
        testing_map.set_chunk(1, 1, biome_chunk)
    with pytest.raises(Exception):
        biome_chunk = BiomeChunk(1, 14, chunk_width)
        testing_map.set_chunk(1, 1, biome_chunk)


@pytest.mark.skip(reason="TODO")
def test_set_get_chunk():
    assert True is True


# TODO more tests for map


@pytest.mark.parametrize("generated_chunks, expected_bounding", [
    ([(0, 0), (1, 1)], Bounding(0, 0, 1, 1)),
    ([(0, 0), (0, 1)], Bounding(0, 0, 0, 1)),
    ([(0, 0), (-5, 1), (-3, 0)], Bounding(-5, 0, 0, 1)),
])
def test_map_bounding(generated_chunks, expected_bounding):
    test_map = Map()
    for point in generated_chunks:
        test_map.set_chunk(ValueChunk(point[0], point[1]))
    assert str(test_map.bounding_chunks()) == str(expected_bounding)


def test_chunk_insertion():
    value_map = Map()
    value_map.set_chunk(ValueChunk(0, 0))
    value_map.set_chunk(ValueChunk(1, 0))
    with pytest.raises(Exception):
        value_map.set_chunk(BiomeChunk(2, 0))

    biome_map = Map()
    biome_map.set_chunk(BiomeChunk(0, 0))
    biome_map.set_chunk(BiomeChunk(1, 0))
    with pytest.raises(Exception):
        biome_map.set_chunk(ValueChunk(2, 0))


def test_get_chunk_type():
    empty_map = Map()
    value_map = Map()
    value_map.set_chunk(ValueChunk(0, 0))
    biome_map = Map()
    biome_map.set_chunk(BiomeChunk(0, 0))
    assert empty_map.chunk_type is None
    assert value_map.chunk_type == 'ValueChunk'
    assert biome_map.chunk_type == 'BiomeChunk'
