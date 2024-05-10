import math
from typing import AnyStr, Optional, Callable, Tuple, Union, List

from PIL import Image

from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.utils import Bounding


def _save_map_as_image(value_map: Map, image_name: AnyStr,
                       get_tile_color: Callable[[Union[float, object], int], Tuple[int, int, int]],
                       bounding: Bounding = None,
                       max_value: Optional[float] = 255.0):
    if bounding is None:
        bounding = value_map.bounding_chunks()
    chunk_width = value_map.chunk_width
    img_w = bounding.right - bounding.left + 1
    img_h = bounding.top - bounding.bottom + 1

    im = Image.new('RGB', (img_w * chunk_width, img_h * chunk_width), "black")  # Create a new black image
    pixels = im.load()
    for cx in range(bounding.left, bounding.right + 1):
        for cy in range(bounding.bottom, bounding.top + 1):
            c = value_map.get_chunk(cx, cy)
            if c is not None:
                for i in range(chunk_width):
                    for j in range(chunk_width):
                        global_x = (cx - bounding.left) * chunk_width + i
                        global_y = (cy - bounding.bottom) * chunk_width + j
                        pixels[global_x, global_y] = get_tile_color(c.tiles[i][j], max_value)
    im.save(image_name + '.png')


def _get_height_color(value: float,
                      max_color_value: Optional[float] = 255.0) -> Tuple[int, int, int]:
    # print(value, max_color_value, 255.0 / max_color_value * value)
    h = math.floor(255.0 / max_color_value * value)
    return h, h, h


def _get_biomes_color(biomes: List[Tuple[float, BiomeType]],
                      max_color_value: Optional[float] = 255.0) -> Tuple[int, int, int]:
    if len(biomes) == 0:
        return 0, 0, 0
    sum_weight = 0
    r, g, b = 0, 0, 0
    for biome in biomes:
        sum_weight += biome[0]
        r += biome[1].rendering_color[0] * biome[0]
        g += biome[1].rendering_color[1] * biome[0]
        b += biome[1].rendering_color[2] * biome[0]
    r = math.floor(255.0 / max_color_value * r / sum_weight)
    g = math.floor(255.0 / max_color_value * g / sum_weight)
    b = math.floor(255.0 / max_color_value * b / sum_weight)
    return r, g, b


def save_height_map_as_image(height_map: Map, image_name: AnyStr, bounding: Bounding = None,
                             max_color_value: Optional[float] = 255.0):
    """ Render and save heightmap region as png image.
    :param height_map: Heightmap to save.
    :param image_name: Name of the image file.
    :param bounding: Rectangle bounding of the map to save (in chunks).
                     If it wasn't specified it will be set as bounding of the whole specified map.
    :param max_color_value: Max height of rendering region which corresponds to white color.
    """
    _save_map_as_image(height_map, image_name, _get_height_color, bounding, max_color_value)


def save_biome_map_as_image(biome_map: Map, image_name: AnyStr, bounding: Bounding = None):
    """ Render and save biome map region as png image.
    :param biome_map: Biome map to save.
    :param image_name: Name of the image file.
    :param bounding: Rectangle bounding of the map to save (in chunks).
                     If it wasn't specified it will be set as bounding of the whole specified map.
    """
    _save_map_as_image(biome_map, image_name, _get_biomes_color, bounding, 255.0)
