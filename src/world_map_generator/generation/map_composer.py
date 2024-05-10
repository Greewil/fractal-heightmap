from typing import Optional, List, Callable, Tuple

import numpy as np

from world_map_generator.default_values import TILES_IN_CHUNK
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import ValueChunk, Chunk
from world_map_generator.utils import get_random_seed
from world_map_generator.utils import is_power_of_two


def base_composing_func(seed: int, tile_x: int, tile_y: int, tiles: List[float | Tuple[float, BiomeType]]) -> float:
    output = 0.0
    for tile in tiles:
        if isinstance(tile, float):
            output += tile
    return output


class MapComposer:
    """ Map composer which composes different chunks tile by tile  using specified method.
    Input chunks could be ValueChunks or BiomeChunks. Resulted chunk will be ValueChunk.

    Attributes:
        seed           Number which is used in procedural generation.
                       If it wasn't specified it will be generated randomly.
        chunk_width    Chunk size which defines tiles matrix.
                       Tile matrix size which should be [chunk_width x chunk_width].
                       Chunk width should be the power of 2.
        composing_func Method will be used to compose different maps tile by tile.
                       Method returns composed value for corresponding tile.
                       Where input parameters are:
                           seed - map composer seed (int),
                           tile_x - tile x (int),
                           tile_y - tile y (int),
                           tiles - list of tiles from maps that should be composed (list).
    """

    def __init__(self, seed: Optional[int] = None,
                 chunk_width: Optional[int] = TILES_IN_CHUNK,
                 composing_func: Callable[[int, int, int, List[float | Tuple[float, BiomeType]]], float]
                 = base_composing_func) -> None:
        """ Map composer which composes different chunks tile by tile  using specified method.
        Input chunks could be ValueChunks or BiomeChunks. Resulted chunk will be ValueChunk.

        :param seed:            Number which is used in procedural generation.
                                If it wasn't specified it will be generated randomly.
        :param chunk_width:     Chunk size which defines tiles matrix.
                                Tile matrix size which should be [chunk_width x chunk_width].
                                Chunk width should be the power of 2.
        :param composing_func:  Method will be used to compose different maps tile by tile.
                                Method returns composed value for corresponding tile.
                                Where input parameters are:
                                    seed - map composer seed (int),
                                    tile_x - tile x (int),
                                    tile_y - tile y (int),
                                    tiles - list of tiles from maps that should be composed (list).
        """
        if seed is None:
            self.seed = get_random_seed()
        else:
            self.seed = seed
        if not is_power_of_two(chunk_width):
            raise Exception("chunk_width should be the power of 2!")
        self._chunk_width = chunk_width
        self._composing_func = composing_func

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

    @property
    def composing_func(self):
        return self._composing_func

    def _clean_value_matrix(self):
        self.value_matrix = np.full((self.chunk_width, self.chunk_width), 0.0)

    def compose_chunks(self, chunk_x: int, chunk_y: int,
                       chunks: List[Chunk] = None) -> ValueChunk:
        """
        Compose chunks tile by tile using composing_func.

        :param chunk_x:         Chunk x position in world
        :param chunk_y:         Chunk y position in world
        :param chunks:          List of chunks which would be composed together into one ValueChunk.
        :return:                Composed ValueChunk of size [chunk_width x chunk_width].
        """
        self._clean_value_matrix()

        for x in range(self.chunk_width):
            for y in range(self.chunk_width):
                tiles = [c.get_tile(x, y) for c in chunks]
                tile_x = x + chunk_x * self.chunk_width
                tile_y = y + chunk_y * self.chunk_width
                self.value_matrix[x, y] = self.composing_func(seed=self.seed, tile_x=tile_x, tile_y=tile_y, tiles=tiles)

        return ValueChunk(chunk_x, chunk_y, self.chunk_width, self.value_matrix)
