import pytest
from numpy.testing import assert_array_equal

from world_map_generator.map.biome import are_biome_tiles_same
from .fixtures.chunks import chunk_width, biome_types, tiles_for_value_chunk  # noqa: F401
from .fixtures.maps import map_bounding, random_value_map, random_biome_map  # noqa: F401

from world_map_generator.map import Map
from world_map_generator.map.chunk import ValueChunk, BiomeChunk
from world_map_generator.map.map import json_to_map
from world_map_generator.utils import Bounding


@pytest.mark.parametrize("chunk_position", [
    (1, 1), (1_000_000_000_000, 1_000_000_000_000), (-1, -10), (-1_000_000_000_000, -1_000_000_000_000)
])
def test_create_value_chunk(chunk_width, chunk_position):
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
def test_create_biome_chunk(chunk_width, chunk_position):
    testing_map = Map(chunk_width=chunk_width)
    testing_map.set_chunk(BiomeChunk(0, 0, chunk_width))  # to set chunk_type
    testing_map.create_chunk(chunk_position[0], chunk_position[1])
    assert testing_map.get_chunk(chunk_position[0], chunk_position[1]) is not None
    assert testing_map.get_chunk(chunk_position[0], chunk_position[1] + 1) is None
    assert testing_map.chunk_type == 'BiomeChunk'


@pytest.mark.parametrize("tiles_input", [
    1.1, 0.0, -5.1, 1.0e100
])
def test_set_get_value_tile(chunk_width, tiles_for_value_chunk, tiles_input):
    testing_map = Map(chunk_width=chunk_width)
    testing_map.set_tile(1, 1, tiles_input)
    assert testing_map.get_tile(1, 1) == tiles_input
    assert testing_map.get_tile(1, 2) == 0.0  # empty tile
    assert testing_map.get_tile(chunk_width, 1) is None  # tile in chunk that wasn't generated yet

    chunk = ValueChunk(1, 1, chunk_width, tiles_for_value_chunk)
    testing_map.set_chunk(chunk)
    assert testing_map.get_tile(chunk_width + 1, chunk_width + 1) == tiles_for_value_chunk[1][1]
    testing_map.set_tile(chunk_width + 1, chunk_width + 1, tiles_input)
    assert testing_map.get_tile(chunk_width + 1, chunk_width + 1) == tiles_input


@pytest.mark.parametrize("tiles_input", [
    1.1, 0.0, -5.1, 1.0e100
])
def test_set_value_tile_updates_chunk_type(chunk_width, tiles_input):
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


def test_convert_value_map_to_json(chunk_width, map_bounding, random_value_map):
    initial_map = random_value_map
    map_as_json = initial_map.to_json(map_bounding)
    map_from_json = json_to_map(map_as_json)
    assert map_from_json.chunk_width == initial_map.chunk_width
    assert map_from_json.chunk_type == initial_map.chunk_type
    assert map_from_json.seed == initial_map.seed
    map_bounding.for_each(lambda x, y: assert_array_equal(initial_map.get_chunk(x, y).tiles,
                                                          map_from_json.get_chunk(x, y).tiles))


def test_convert_biome_map_to_json(chunk_width, map_bounding, biome_types, random_biome_map):
    initial_map = random_biome_map
    map_as_json = initial_map.to_json(map_bounding)
    map_from_json = json_to_map(map_as_json, biome_types)
    assert map_from_json.chunk_width == initial_map.chunk_width
    assert map_from_json.chunk_type == initial_map.chunk_type
    assert map_from_json.seed == initial_map.seed

    def assert_biome_chunks_same(chunk1, chunk2):
        assert chunk1.chunk_width == chunk2.chunk_width
        assert chunk1.chunk_type == chunk2.chunk_type
        assert chunk1.position == chunk2.position
        for i in range(chunk1.chunk_width):
            for j in range(chunk2.chunk_width):
                assert are_biome_tiles_same(chunk1.get_tile(i, j), chunk2.get_tile(i, j)) is True

    map_bounding.for_each(lambda x, y: assert_biome_chunks_same(initial_map.get_chunk(x, y),
                                                                map_from_json.get_chunk(x, y)))
