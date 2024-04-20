from typing import Optional

import numpy as np

from world_map_generator.default_values import TILES_IN_CHUNK
from world_map_generator.map.chunk import ValueChunk, BiomeChunk
from world_map_generator.utils import get_random_seed
from world_map_generator.utils import get_position_seed, is_power_of_two


class MapModifier:
    """ Heightmap modifier which uses biomes map to apply corresponding height_modification.

    Attributes:
        seed               Number which is used in procedural generation.
                           If it wasn't specified it will be generated randomly.
        chunk_width        Chunk size which defines tiles matrix.
                           Tile matrix size which should be [chunk_width x chunk_width].
                           Chunk width should be the power of 2.
    """

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = TILES_IN_CHUNK) -> None:
        """ Heightmap modifier which uses biomes map to apply corresponding height_modification.
        :param seed:        Number which is used in procedural generation.
                            If it wasn't specified it will be generated randomly.
        :param chunk_width: Chunk size which defines tiles matrix.
                            Tile matrix size which should be [chunk_width x chunk_width].
                            Chunk width should be the power of 2.
        """
        if seed is None:
            self.seed = get_random_seed()
        else:
            self.seed = seed
        if not is_power_of_two(chunk_width):
            raise Exception("chunk_width should be the power of 2!")
        self._chunk_width = chunk_width

        self._clean_value_matrix()

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value: int):
        self._seed = value % (2 ** 32)

    @property
    def chunk_width(self):
        return self._chunk_width

    def _generate_random_sequence(self, x: int, y: int):
        pos_seed = get_position_seed(x, y, self.seed)
        np.random.seed(pos_seed)
        self._random_sequence = np.random.rand(self.chunk_width, self.chunk_width)

    def _clean_value_matrix(self):
        self.value_matrix = np.full((self.chunk_width, self.chunk_width), 0.0)

    def modify_heightmap_chunk(self, chunk_x: int, chunk_y: int,
                               heightmap_chunk: ValueChunk,
                               biome_chunk: BiomeChunk) -> np.ndarray:
        """
        From heightmap_chunk create chunk of modified heights according to biome chunk modification functions.

        :param chunk_x: chunk x position in world
        :param chunk_y: chunk y position in world
        :param heightmap_chunk: heightmap chunk from which will be created modified chunk.
        :param biome_chunk: biome chunk which will be used to modify heightmap (using height_modification methods).
        :return: modified heightmap chunk values (numpy matrix of size [chunk_width x chunk_width]).
        """
        # self._generate_random_sequence(chunk_x, chunk_y)
        # TODO force height_modification to use either seed or generated random value
        self._clean_value_matrix()

        for x in range(self.chunk_width):
            for y in range(self.chunk_width):
                h = heightmap_chunk.get_tile(x, y)
                average_value = 0.0
                total_weight = 0.0
                for b in biome_chunk.get_tile(x, y):
                    total_weight += b[0]
                    average_value += b[0] * b[1].height_modification(h, b[1].biome_parameters)
                if total_weight != 0:
                    self.value_matrix[x, y] = average_value / total_weight

        return self.value_matrix
