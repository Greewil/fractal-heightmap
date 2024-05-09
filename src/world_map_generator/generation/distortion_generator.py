import math
from typing import Optional, List, Callable, Tuple

import numpy as np

from world_map_generator.default_values import TILES_IN_CHUNK
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import ValueChunk, BiomeChunk, Chunk
from world_map_generator.utils import get_random_seed
from world_map_generator.utils import get_position_seed, is_power_of_two


class DistortionGenerator:
    """ Tool for map distortion which uses two shift maps for x-axis and y-axis.

    Attributes:
        chunk_width             Chunk size which defines tiles matrix.
                                Tile matrix size which should be [chunk_width x chunk_width].
                                Chunk width should be the power of 2.
        distortion_amplitude    Shift that will ba applied in tile with 1.0 values in shift map.
    """

    def __init__(self, chunk_width: Optional[int] = TILES_IN_CHUNK,
                 distortion_amplitude: int = TILES_IN_CHUNK) -> None:
        """ Tool for map distortion which uses two shift maps for x-axis and y-axis.

        :param chunk_width:          Chunk size which defines tiles matrix.
                                     Tile matrix size which should be [chunk_width x chunk_width].
                                     Chunk width should be the power of 2.
        :param distortion_amplitude: Shift that will ba applied in tile with 1.0 values in shift map.
        """
        if not is_power_of_two(chunk_width):
            raise Exception("chunk_width should be the power of 2!")
        self._chunk_width = chunk_width
        self._distortion_amplitude = distortion_amplitude

        self._clean_value_matrix()

    @property
    def chunk_width(self):
        return self._chunk_width

    @property
    def distortion_amplitude(self):
        return self._distortion_amplitude

    def _clean_value_matrix(self):
        self.value_matrix = np.full((self.chunk_width, self.chunk_width), 0.0)

    def distort_map_chunk(self, chunk_x: int, chunk_y: int, value_map: Map = None,
                       shift_x_chunk: ValueChunk = None, shift_y_chunk: ValueChunk = None) -> ValueChunk:
        """
        Distort specified chunk of the value_map which uses two shift maps for x-axis and y-axis.

        :param chunk_x:             Chunk x position in world.
        :param chunk_y:             Chunk y position in world.
        :param value_map:           List of chunks which would be composed together into one ValueChunk.
        :param shift_x_chunk:       Chunk with values to distort x-axis.
        :param shift_y_chunk:       Chunk with values to distort y-axis.
        :return:                    Composed ValueChunk of size [chunk_width x chunk_width].
        """
        self._clean_value_matrix()

        for x in range(self.chunk_width):
            for y in range(self.chunk_width):
                tile_x = x + chunk_x * self.chunk_width
                tile_y = y + chunk_y * self.chunk_width
                old_tile_x = math.floor(tile_x + self.distortion_amplitude * shift_x_chunk.get_tile(x, y))
                old_tile_y = math.floor(tile_y + self.distortion_amplitude * shift_y_chunk.get_tile(x, y))
                self.value_matrix[x, y] = value_map.get_tile(old_tile_x, old_tile_y)

        return ValueChunk(chunk_x, chunk_y, self.chunk_width, self.value_matrix)
