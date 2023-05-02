from typing import AnyStr, Optional

import numpy as np

from new_src.default_values import *
from new_src.utils import Bounding
from new_src.utils.utils import get_random_seed
from .chunk import Chunk


class Map:

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = TILES_IN_CHUNK):
        self._chunk_width = chunk_width
        self._seed = seed
        self.chunks = {}

    @property
    def chunk_width(self):
        return self._chunk_width

    @property
    def seed(self):
        return self._seed

    def get_chunk(self, x: int, y: int) -> Chunk:
        return self.chunks.get(str((x, y)), None)

    def set_chunk(self, chunk: Chunk):
        self.chunks[str(chunk.position)] = chunk

    def create_chunk(self, x: int, y: int):
        """ Create blank chunk if its not exist. """
        if not self.is_chunk_exists(x, y):
            self.chunks[str((x, y))] = Chunk(x, y, self.chunk_width)

    def delete_chunk(self, x: int, y: int):
        if self.chunks.get(str((x, y))) is not None:
            self.chunks.pop(str((x, y)))

    def delete_all_chunks(self):
        self.chunks = {}

    def is_chunk_exists(self, x: int, y: int) -> bool:
        chunk = self.chunks.get(str((x, y)))
        return True if chunk is not None else False

    def get_tile(self, x: int, y: int) -> float:
        chunk_x = x // self.chunk_width
        chunk_y = y // self.chunk_width
        checking_chunk = self.get_chunk(chunk_x, chunk_y)
        if checking_chunk is not None:
            return checking_chunk.get_tile(x % self.chunk_width, y % self.chunk_width)
        else:
            return None

    def set_tile(self, x: int, y: int, tile: float):
        chunk_x = x // self.chunk_width
        chunk_y = y // self.chunk_width
        self.create_chunk(chunk_x, chunk_y)
        chunk = self.get_chunk(chunk_x, chunk_y)
        chunk.set_tile(x % self.chunk_width, y % self.chunk_width, tile)

    def number_of_generated_tiles(self) -> int:
        return len(self.chunks.keys()) * self.chunk_width * self.chunk_width

    def bounding_chunks(self) -> Bounding:
        """
        :return: bounding in chunks or None if there is no chunks in map
        """
        bounding = Bounding(1, 1, -1, -1)
        if len(self.chunks.keys()) == 0:
            return None
        for k, c in self.chunks.items():
            if c.position[0] > bounding.right:
                bounding.right = c.position[0]
            if c.position[0] < bounding.left:
                bounding.left = c.position[0]
            if c.position[1] > bounding.top:
                bounding.top = c.position[1]
            if c.position[1] < bounding.bottom:
                bounding.bottom = c.position[1]
        return bounding

    def bounding_tiles(self) -> Bounding:
        """
        :return: bounding in tiles or None if there is no chunks in map
        """
        bounding = self.bounding_chunks()
        if bounding is None:
            return None
        bounding.left *= self.chunk_width
        bounding.right = (bounding.right + 1) * self.chunk_width
        bounding.top = (bounding.top + 1) * self.chunk_width
        bounding.bottom *= self.chunk_width
        return bounding

    def __str__(self) -> AnyStr:
        return '{"seed": ' + str(self.seed) + \
               ', "chunks": [' + ', '.join(str(x) for k, x in self.chunks.items()) + ']}'
