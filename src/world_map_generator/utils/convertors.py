import json
from typing import List, Tuple

from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import ValueChunk, Chunk, BiomeChunk
from world_map_generator.utils import Bounding


def _value_chunk_to_dict(chunk: ValueChunk) -> dict:
    tiles = [[0.0 for i in range(chunk.chunk_width)] for j in range(chunk.chunk_width)]
    for x in range(chunk.chunk_width):
        for y in range(chunk.chunk_width):
            tiles[x][y] = chunk.get_tile(x, y)
    chunk_dict = {
        "x": chunk.position[0],
        "y": chunk.position[1],
        "tiles": tiles,
    }
    return chunk_dict


def _biome_tile_to_dict(biome_tile: List[Tuple[float, BiomeType]]) -> dict:
    output = {}
    for biome in biome_tile:
        output[biome[1]] = biome[0]
    return output


def _biome_chunk_to_dict(chunk: BiomeChunk) -> dict:
    tiles = [[{} for i in range(chunk.chunk_width)] for j in range(chunk.chunk_width)]
    for x in range(chunk.chunk_width):
        for y in range(chunk.chunk_width):
            tiles[x][y] = _biome_tile_to_dict(chunk.get_tile(x, y))
    chunk_dict = {
        "x": chunk.position[0],
        "y": chunk.position[1],
        "tiles": tiles,
    }
    return chunk_dict


def chunk_to_dict(chunk: Chunk) -> dict:
    if isinstance(chunk, ValueChunk):
        return _value_chunk_to_dict(chunk)
    elif isinstance(chunk, BiomeChunk):
        return _biome_chunk_to_dict(chunk)


def chunk_to_json(chunk: ValueChunk) -> str:
    return json.dumps(chunk_to_dict(chunk))


def _json_to_chunk(chunk_as_json: str, chunk_type: str) -> ValueChunk | BiomeChunk:
    """ TODO """
    chunk_as_dict = json.loads(chunk_as_json)
    tiles = chunk_as_dict["tiles"]
    chunk_width = len(tiles)
    chunk = ValueChunk(chunk_as_dict["x"], chunk_as_dict["y"], chunk_width)
    for x in range(chunk.chunk_width):
        for y in range(chunk.chunk_width):
            chunk.tiles[x][y] = tiles[x][y]
            # TODO check chunk_type and return biome chunk if needed
    return chunk


def json_to_value_chunk(chunk_as_json: str) -> ValueChunk:
    return _json_to_chunk(chunk_as_json, "value")


def json_to_biome_chunk(chunk_as_json: str) -> ValueChunk:
    return _json_to_chunk(chunk_as_json, "biome")


def value_chunk_array_to_json(chunks: List[ValueChunk]) -> str:
    chunks_as_dict = [chunk_to_dict(c) for c in chunks]
    return json.dumps(chunks_as_dict)


# TODO json_to_value_chunk_array


def map_to_json(map_to_convert: Map, map_type: str, chunks_bounding: Bounding = None) -> str:
    """ TODO modify docs from below """
    if map_type is None:
        Exception("Map type not specified")
    if chunks_bounding is None:
        chunks_bounding = map_to_convert.bounding_chunks()
    tiles_x_size = map_to_convert.chunk_width * (chunks_bounding.right - chunks_bounding.left)
    tiles_y_size = map_to_convert.chunk_width * (chunks_bounding.top - chunks_bounding.bottom)
    chunks_list = []
    for i in range(chunks_bounding.left, chunks_bounding.right):
        for j in range(chunks_bounding.bottom, chunks_bounding.top):
            chunk = map_to_convert.get_chunk(i, j)
            if chunk is not None:
                chunks_list.append(chunk)
    chunks_as_dict = [chunk_to_dict(c) for c in chunks_list]
    map_dict = {
        "seed": map_to_convert.seed,
        "chunk_width": map_to_convert.chunk_width,
        "chunks_bounding": vars(chunks_bounding),
        "region_width_in_tiles": tiles_x_size,
        "region_height_in_tiles": tiles_y_size,
        "map_type": map_type,
        "chunks": chunks_as_dict,
    }
    return json.dumps(map_dict)


def map_region_to_json(map_to_convert: Map, map_type: str, chunks_bounding: Bounding = None) -> str:
    """
    Converts map region in bounding to json string. This method stores tiles in json string as single matrix of size
    [bounding_width_in_tiles x bounding_height_in_tiles].

    :param map_to_convert: Biome chunk which will be used to modify heightmap (using height_modification methods).
    :param chunks_bounding: Bounding of chunks which will be converted to json string.
    :return: JSON string with map parameters. This method stores tiles in json string as single matrix of size
             [bounding_width_in_tiles x bounding_height_in_tiles].
    """
    if map_type is None:
        Exception("Map type not specified")
    if chunks_bounding is None:
        chunks_bounding = map_to_convert.bounding_chunks()
    tiles_x_size = map_to_convert.chunk_width * (chunks_bounding.right - chunks_bounding.left)
    tiles_y_size = map_to_convert.chunk_width * (chunks_bounding.top - chunks_bounding.bottom)
    tiles = [[0.0 for i in range(tiles_y_size)] for j in range(tiles_x_size)]
    for i in range(chunks_bounding.left, chunks_bounding.right):
        for j in range(chunks_bounding.bottom, chunks_bounding.top):
            chunk = map_to_convert.get_chunk(i, j)
            if chunk is None:
                continue
            for x in range(map_to_convert.chunk_width):
                for y in range(map_to_convert.chunk_width):
                    relative_x = x + map_to_convert.chunk_width * (i - chunks_bounding.left)
                    relative_y = y + map_to_convert.chunk_width * (j - chunks_bounding.bottom)
                    cur_tile = chunk.get_tile(x, y)
                    if isinstance(cur_tile, float):
                        tiles[relative_x][relative_y] = cur_tile
                    elif isinstance(cur_tile, tuple):
                        tiles[relative_x][relative_y] = _biome_tile_to_dict(cur_tile)
                    else:
                        Exception(f"can't convert tile type: {type(cur_tile)}")
                    # TODO check if its biome or value map
    tiles_left = chunks_bounding.left * map_to_convert.chunk_width
    tiles_right = tiles_left + tiles_x_size
    tiles_bottom = chunks_bounding.bottom * map_to_convert.chunk_width
    tiles_top = tiles_bottom + tiles_y_size
    map_region = {
        "seed": map_to_convert.seed,
        "tiles_left": tiles_left,
        "tiles_right": tiles_right,
        "tiles_bottom": tiles_bottom,
        "tiles_top": tiles_top,
        "region_width_in_tiles": tiles_x_size,
        "region_height_in_tiles": tiles_y_size,
        "chunk_width": map_to_convert.chunk_width,
        "map_type": map_type,
        "tiles": tiles,
    }
    return json.dumps(map_region)

# TODO biome_chunk_to_json
# TODO json_to_biome_chunk
# TODO biome_chunk_array_to_json
# TODO json_to_biome_chunk_array

# def save_tile_rectangle_as_binary(self, bounding: Bounding):
#     tiles_x_size = self.chunk_width * (bounding.right - bounding.left)
#     tiles_y_size = self.chunk_width * (bounding.top - bounding.bottom)
#     tiles = [[0.0 for i in range(tiles_x_size)] for j in range(tiles_y_size)]
#     for i in range(0, bounding.right - bounding.left):
#         for j in range(0, bounding.top - bounding.bottom):
#             chunk = self.get_chunk(i, j)
#             for x in range(self.chunk_width):
#                 for y in range(self.chunk_width):
#                     tiles[x + i * self.chunk_width][y + j * self.chunk_width] = chunk.get_tile(x, y)
#
#     with open('map.bin', 'wb') as file:
#         for i in range(0, bounding.right - bounding.left):
#             for j in range(0, bounding.top - bounding.bottom):
#                 file.write(struct.pack('<f', tiles[x + i * self.chunk_width][y + j * self.chunk_width]))
