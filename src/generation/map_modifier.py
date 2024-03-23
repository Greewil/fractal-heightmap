import math
from typing import Optional, List

import numpy as np

from src.default_values import *
from src.map.chunk import ValueChunk, BiomeChunk
from src.utils import Bounding, get_random_seed
from src.utils import get_position_seed, is_power_of_two


class MapModifier:

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = TILES_IN_CHUNK) -> None:
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
                               biome_chunk: BiomeChunk):
        # self._generate_random_sequence(chunk_x, chunk_y)
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
