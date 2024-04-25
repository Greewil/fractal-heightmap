from typing import AnyStr, Optional, List, Tuple, Any

import numpy as np

from world_map_generator.default_values import TILES_IN_CHUNK
from world_map_generator.map.biome import BASE_BIOME_TYPE, BiomeType


class Chunk:
    """Chunk with tiles packed in numpy matrix.

    Attributes:
        x               Global x position in chunk grid.
        y               Global y position in chunk grid.
        chunk_width     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        tiles           Matrix of float values packed in numpy matrix with size [chunk_width x chunk_width].
    """

    def __init__(self, x: int, y: int, chunk_width: Optional[int] = TILES_IN_CHUNK,
                 tiles: Optional[np.ndarray[Any, np.dtype]] = None):
        """Chunk with tiles packed in numpy matrix.
        :param x:               Global x position in chunk grid.
        :param y:               Global y position in chunk grid.
        :param chunk_width:     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        :param tiles:           Matrix of float values packed in numpy matrix with size [chunk_width x chunk_width].
        """
        self.position = (x, y)
        self._chunk_width = chunk_width
        if tiles is not None:
            self.tiles = tiles
        else:
            self.tiles = np.full((self.chunk_width, self.chunk_width), 0.0)

    @property
    def chunk_width(self):
        return self._chunk_width

    def get_tile(self, x: int, y: int) -> float:
        return self.tiles[x][y]

    def set_tile(self, x: int, y: int, value: float):
        self.tiles[x][y] = value

    def __str__(self) -> AnyStr:
        output = '{"chunk_width": ' + str(self.chunk_width)
        output += ', "position": ' + str(self.position)

        # output += ', "tiles": ['
        # for i in range(self.chunk_width):
        #     for j in range(self.chunk_width - 1):
        #         output += str(self.tiles[i, j]) + ', '
        # output += str(self.tiles[self.chunk_width - 1, self.chunk_width - 1]) + ']'

        output += "}"
        return output


class ValueChunk(Chunk):
    """Chunk with tiles packed in numpy matrix.

    Attributes:
        x               Global x position in chunk grid.
        y               Global y position in chunk grid.
        chunk_width     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        tiles           Matrix of float values packed in numpy matrix with size [chunk_width x chunk_width].
    """

    def __init__(self, x: int, y: int, chunk_width: Optional[int] = TILES_IN_CHUNK,
                 tiles: Optional[np.ndarray[Any, np.dtype]] = None):
        """Chunk with tiles packed in numpy matrix.
        :param x:               Global x position in chunk grid.
        :param y:               Global y position in chunk grid.
        :param chunk_width:     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        :param tiles:           Matrix of float values packed in numpy matrix with size [chunk_width x chunk_width].
        """
        if tiles is not None:
            pass
            # TODO handle situations in which tiles are not [chunk_width x chunk_width] size
        super().__init__(x, y, chunk_width, tiles)
        if self.tiles is None:
            self.tiles = np.full((self.chunk_width, self.chunk_width), 0.0)


class BiomeChunk(Chunk):
    """Chunk with information about biomes types and their weights in tiles.

    Attributes:
        x               Global x position in chunk grid.
        y               Global y position in chunk grid.
        chunk_width     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        tiles           Matrix of biome types information with size [chunk_width x chunk_width].
                        Each tile is a list of tuples.
                        First element of each tuple is biome type weight and second is BiomeType.
    """

    def __init__(self, x: int, y: int, chunk_width: Optional[int] = TILES_IN_CHUNK,
                 tiles: Optional[List[List[List[Tuple[float, BiomeType]]]]] = None):
        """Chunk with information about biomes types and their weights in tiles.
        :param x:               Global x position in chunk grid.
        :param y:               Global y position in chunk grid.
        :param chunk_width:     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        :param tiles:           Matrix of biome types information with size [chunk_width x chunk_width].
                                Each tile is a list of tuples.
                                First element of each tuple is biome type weight and second is BiomeType.
        """
        super().__init__(x, y, chunk_width, tiles)
        if self.tiles is None:
            self.tiles = [[[(1, BASE_BIOME_TYPE)]] * self.chunk_width for _ in range(chunk_width)]
