import json
from typing import List

from world_map_generator.map import Map
from world_map_generator.map.chunk import ValueChunk
from world_map_generator.utils import Bounding


def value_chunk_to_json(chunk: ValueChunk) -> str:
    tiles = [[0.0 for i in range(chunk.chunk_width)] for j in range(chunk.chunk_width)]
    for x in range(chunk.chunk_width):
        for y in range(chunk.chunk_width):
            tiles[x][y] = chunk.get_tile(x, y)
    chunk_dict = {
        "x": chunk.position[0],
        "y": chunk.position[1],
        "tiles": tiles,
    }
    return json.dumps(chunk_dict)


def json_to_value_chunk(chunk_as_json: str) -> ValueChunk:
    chunk_as_dict = json.loads(chunk_as_json)
    tiles = chunk_as_dict["tiles"]
    chunk_width = len(tiles)
    chunk = ValueChunk(chunk_as_dict["x"], chunk_as_dict["y"], chunk_width)
    for x in range(chunk.chunk_width):
        for y in range(chunk.chunk_width):
            chunk.tiles[x][y] = tiles[x][y]
    return chunk


def value_chunk_array_to_json(chunks: List[ValueChunk]) -> str:
    chunks_as_dict = [value_chunk_to_json(c) for c in chunks]
    return json.dumps(chunks_as_dict)


def map_region_to_json(value_map: Map, bounding: Bounding) -> str:
    tiles_x_size = value_map.chunk_width * (bounding.right - bounding.left)
    tiles_y_size = value_map.chunk_width * (bounding.top - bounding.bottom)
    tiles = [[0.0 for i in range(tiles_y_size)] for j in range(tiles_x_size)]
    for i in range(bounding.left, bounding.right):
        for j in range(bounding.bottom, bounding.top):
            chunk = value_map.get_chunk(i, j)
            if chunk is None:
                continue
            for x in range(value_map.chunk_width):
                for y in range(value_map.chunk_width):
                    relative_x = x + value_map.chunk_width * (i - bounding.left)
                    relative_y = y + value_map.chunk_width * (j - bounding.bottom)
                    tiles[relative_x][relative_y] = chunk.get_tile(x, y)
    tiles_left = bounding.left * value_map.chunk_width
    tiles_right = tiles_left + tiles_x_size
    tiles_bottom = bounding.bottom * value_map.chunk_width
    tiles_top = tiles_bottom + tiles_y_size
    map_region = {
        "tiles_left": tiles_left,
        "tiles_right": tiles_right,
        "tiles_bottom": tiles_bottom,
        "tiles_top": tiles_top,
        "chunk_width": value_map.chunk_width,
        "tiles": tiles,
    }
    return json.dumps(map_region)

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
