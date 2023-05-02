from typing import AnyStr, Optional, List

import numpy as np

from src.default_values import *


class Chunk:

    def __init__(self, x: int, y: int, chunk_width: Optional[int] = TILES_IN_CHUNK,
                 tiles: Optional[List[List[float]]] = None):
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
        return self.tiles[x, y]

    def set_tile(self, x: int, y: int, value: float):
        self.tiles[x, y] = value

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
