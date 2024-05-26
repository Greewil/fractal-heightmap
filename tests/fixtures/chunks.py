from math import floor

import numpy as np
import pytest

from world_map_generator.map.biome import BiomeType


@pytest.fixture
def chunk_width():
    return 16


@pytest.fixture
def biome_types():
    biome_type_1 = BiomeType("biome 1", biome_parameters={"param 1": 1.1})
    biome_type_2 = BiomeType("biome 2", biome_parameters={"param 2": 0.5})
    biome_type_3 = BiomeType("biome 3", biome_parameters={"param 1": 0.75, "param 2": 0.5})
    return [biome_type_1, biome_type_2, biome_type_3]


@pytest.fixture
def tiles_for_value_chunk(chunk_width, biome_types):
    return np.random.rand(chunk_width * chunk_width).reshape((chunk_width, chunk_width))


@pytest.fixture
def tiles_for_biome_chunk(chunk_width, biome_types):
    random_values = np.random.rand(chunk_width * chunk_width).reshape((chunk_width, chunk_width))
    tiles = []
    for i in range(chunk_width):
        tiles.append([])
        for j in range(chunk_width):
            tile = []
            for k in range(floor(3 * random_values[i][j])):
                tile.append((random_values[i][j], biome_types[k]))
            tiles[i].append(tile)
    return tiles
