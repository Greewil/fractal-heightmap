from typing import Optional

from world_map_generator.default_values import TILES_IN_CHUNK
from world_map_generator.utils import get_random_seed, is_power_of_two


class ChunkGenerator:
    """ Generator of value map chunks.

    Attributes:
        seed                        Number which is used in procedural generation.
                                    If it wasn't specified it will be generated randomly.
        chunk_width                 Chunk size which defines tiles matrix.
                                    Tile matrix size which should be [chunk_width x chunk_width].
                                    Chunk width should be the power of 2.
    """

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = TILES_IN_CHUNK) -> None:
        """ Generator of value map chunks.
        :param seed:                Number which is used in procedural generation.
                                    If it wasn't specified it will be generated randomly.
        :param chunk_width:         Chunk size which defines tiles matrix.
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

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value: int):
        self._seed = value % (2 ** 32)

    @property
    def chunk_width(self):
        return self._chunk_width
