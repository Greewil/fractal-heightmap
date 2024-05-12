import json
from typing import AnyStr, Optional, Union, Callable, List

from world_map_generator.default_values import TILES_IN_CHUNK
from world_map_generator.utils import Bounding
from world_map_generator.utils import get_random_seed
from .biome import biome_tile_to_dict, BiomeType
from .chunk import Chunk, chunk_dict_to_chunk


class Map:
    """ Collection of chunks, which are generated with specified seed.

    Attributes:
        seed               Number which is used in procedural generation.
                           If it wasn't specified it will be generated randomly.
        chunk_type         TODO Chunk size which defines tiles matrix.
        chunk_width        Chunk size which defines tiles matrix.
                           Tile matrix size which should be [chunk_width x chunk_width].
                           Chunk width should be the power of 2.
        chunks             Dict of chunks where hash based on chunk position (str((x, y))).
    """

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = TILES_IN_CHUNK):
        """ Collection of chunks, which are generated with specified seed.
        :param seed:        Number which is used in procedural generation.
                            If it wasn't specified it will be generated randomly.
        :param chunk_width: Chunk size which defines tiles matrix.
                            Tile matrix size which should be [chunk_width x chunk_width].
                            Chunk width should be the power of 2.
        """
        self._chunk_width = chunk_width
        if seed is None:
            self._seed = get_random_seed()
        else:
            self._seed = seed % (2**32)
        self.chunks = {}

    @property
    def chunk_width(self):
        return self._chunk_width

    @property
    def seed(self):
        return self._seed

    @property
    def chunk_type(self):
        if self.chunks is None or len(self.chunks) == 0:
            return None
        first_chunk = next(iter(self.chunks))
        if first_chunk is None:
            return None
        else:
            return self.chunks[first_chunk].chunk_type

    def get_chunk(self, x: int, y: int) -> Chunk | None:
        return self.chunks.get(str((x, y)), None)

    def set_chunk(self, chunk: Chunk):
        if self.chunk_type is not None and chunk.chunk_type is not self.chunk_type:
            raise Exception(f"Map chunks should have same types. You trying to add chunk with type {chunk.chunk_type}, "
                            f"but map already has chunks with types {self.chunk_type}")
        self.chunks[str(chunk.position)] = chunk

    def create_chunk(self, x: int, y: int):
        """ Create blank chunk if it's not exist. """
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

    def get_tile(self, x: int, y: int) -> Union[float, object]:
        chunk_x = x // self.chunk_width
        chunk_y = y // self.chunk_width
        checking_chunk = self.get_chunk(chunk_x, chunk_y)
        if checking_chunk is not None:
            return checking_chunk.get_tile(x % self.chunk_width, y % self.chunk_width)
        else:
            return None

    def set_tile(self, x: int, y: int, tile: Union[float, object]):
        chunk_x = x // self.chunk_width
        chunk_y = y // self.chunk_width
        self.create_chunk(chunk_x, chunk_y)
        chunk = self.get_chunk(chunk_x, chunk_y)
        chunk.set_tile(x % self.chunk_width, y % self.chunk_width, tile)

    def number_of_generated_tiles(self) -> int:
        return self.number_of_generated_chunks() * self.chunk_width * self.chunk_width

    def number_of_generated_chunks(self) -> int:
        return len(self.chunks.keys())

    def bounding_chunks(self) -> Bounding | None:
        """
        :return: bounding in chunks or None if there is no chunks in map
        """
        if len(self.chunks.keys()) == 0:
            return None
        first_chunk = next(iter(self.chunks.values()))
        bounding = Bounding(first_chunk.position[0], first_chunk.position[1],
                            first_chunk.position[0], first_chunk.position[1])
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

    def bounding_tiles(self) -> Bounding | None:
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

    def for_each_chunk(self, func: Callable[[Chunk], None]):
        """ Runs functions for each chunk in map. """
        for chunk in self.chunks.itervalues():
            func(chunk)

    def __str__(self) -> AnyStr:
        return '{"seed": ' + str(self.seed) + \
               ', "chunks": [' + ', '.join(str(x) for k, x in self.chunks.items()) + ']}'

    def to_json(self, chunks_bounding: Bounding = None) -> str:
        """
        Converts map in bounding to json string. This method will save each chunk separately.

        :param chunks_bounding: Bounding of chunks which will be converted saved in json string.
        :return: JSON string with map parameters (seed, chunk_width, chunks_bounding, region_width_in_tiles,
                 region_height_in_tiles, map_chunks_type, chunks).
        """
        if chunks_bounding is None:
            chunks_bounding = self.bounding_chunks()
        tiles_x_size = self.chunk_width * (chunks_bounding.right - chunks_bounding.left)
        tiles_y_size = self.chunk_width * (chunks_bounding.top - chunks_bounding.bottom)
        chunks_list = []
        for i in range(chunks_bounding.left, chunks_bounding.right):
            for j in range(chunks_bounding.bottom, chunks_bounding.top):
                chunk = self.get_chunk(i, j)
                if chunk is not None:
                    chunks_list.append(chunk)
        chunks_as_dict = [c.to_dict() for c in chunks_list]
        map_dict = {
            "seed": self.seed,
            "chunk_width": self.chunk_width,
            "chunks_bounding": vars(chunks_bounding),
            "region_width_in_tiles": tiles_x_size,
            "region_height_in_tiles": tiles_y_size,
            "chunk_type": self.chunk_type,
            "chunks": chunks_as_dict,
        }
        return json.dumps(map_dict)

    def to_json_as_one_tile_matrix(self, chunks_bounding: Bounding = None) -> str:
        """
        Converts map region in bounding to json string. This method stores tiles in json string as single matrix of size
        [bounding_width_in_tiles x bounding_height_in_tiles].

        :param chunks_bounding: Bounding of chunks which will be converted to json string.
        :return: JSON string with map parameters (seed, tiles_bounding, region_width_in_tiles, region_height_in_tiles,
                 map_chunks_type, tiles). This method stores tiles in json string as single matrix of size
                 [bounding_width_in_tiles x bounding_height_in_tiles].
        """
        if chunks_bounding is None:
            chunks_bounding = self.bounding_chunks()
        tiles_x_size = self.chunk_width * (chunks_bounding.right - chunks_bounding.left)
        tiles_y_size = self.chunk_width * (chunks_bounding.top - chunks_bounding.bottom)
        tiles = [[0.0 for i in range(tiles_y_size)] for j in range(tiles_x_size)]
        for i in range(chunks_bounding.left, chunks_bounding.right):
            for j in range(chunks_bounding.bottom, chunks_bounding.top):
                chunk = self.get_chunk(i, j)
                if chunk is None:
                    continue
                for x in range(self.chunk_width):
                    for y in range(self.chunk_width):
                        relative_x = x + self.chunk_width * (i - chunks_bounding.left)
                        relative_y = y + self.chunk_width * (j - chunks_bounding.bottom)
                        cur_tile = chunk.get_tile(x, y)
                        if self.chunk_type == 'ValueChunk':
                            tiles[relative_x][relative_y] = cur_tile
                        elif self.chunk_type == 'BiomeChunk':
                            tiles[relative_x][relative_y] = biome_tile_to_dict(cur_tile)
                        else:
                            Exception(f"can't convert tile type: {type(cur_tile)}")
        tiles_left = chunks_bounding.left * self.chunk_width
        tiles_right = tiles_left + tiles_x_size
        tiles_bottom = chunks_bounding.bottom * self.chunk_width
        tiles_top = tiles_bottom + tiles_y_size
        tiles_bounding = Bounding(tiles_left, tiles_bottom, tiles_right, tiles_top)
        map_region = {
            "seed": self.seed,
            "tiles_bounding": vars(tiles_bounding),
            "region_width_in_tiles": tiles_x_size,
            "region_height_in_tiles": tiles_y_size,
            "chunk_width": self.chunk_width,
            "chunk_type": self.chunk_type,
            "tiles": tiles,
        }
        return json.dumps(map_region)


def map_as_dict_to_map(map_as_dict: dict, biomes_list: List[BiomeType]) -> Map:
    """
    TODO


    :param biomes_list: List of all possible biome types used in map (in case if map filled with BiomeChunks).
    """
    seed = map_as_dict["seed"]
    chunk_width = map_as_dict["chunk_width"]
    chunks = map_as_dict["chunks"]
    converted_map = Map(seed, chunk_width)
    for c in chunks:
        converted_map.set_chunk(chunk_dict_to_chunk(c, biomes_list))
    return converted_map


def json_to_map(map_as_json: str) -> Map:
    map_as_dict = json.loads(map_as_json)
    return map_as_dict_to_map(map_as_dict)
