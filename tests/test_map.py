import numpy as np
import pytest
from numpy.testing import assert_array_equal

from world_map_generator.map import Map
from world_map_generator.map.chunk import ValueChunk, chunk_dict_to_chunk, BiomeChunk
from world_map_generator.utils import Bounding


@pytest.mark.skip(reason="TODO")
def test_get_tile():
    assert True is True


@pytest.mark.skip(reason="TODO")
def test_get_chunk():
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
