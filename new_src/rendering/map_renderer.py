import math
from typing import AnyStr, Optional

from PIL import Image

from new_src.map import Map
from new_src.utils.bounding import Bounding


def save_map_as_image(value_map: Map, image_name: AnyStr, bounding: Bounding = None, max_value: Optional[int] = 255):
    if bounding is None:
        bounding = value_map.bounding_chunks()
    chunk_width = value_map.chunk_width
    img_w = bounding.right - bounding.left + 1
    img_h = bounding.top - bounding.bottom + 1
    print('rendering image size', img_w, img_h)
    print('bounding in chunks', str(bounding))

    im = Image.new('RGB', (img_w * chunk_width, img_h * chunk_width), "black")  # Create a new black image
    pixels = im.load()
    for cx in range(bounding.left, bounding.right + 1):
        for cy in range(bounding.bottom, bounding.top + 1):
            c = value_map.get_chunk(cx, cy)
            if c is not None:
                for i in range(chunk_width):
                    for j in range(chunk_width):
                        h = math.floor(255.0 / max_value * c.tiles[i][j])
                        global_x = (cx - bounding.left) * chunk_width + i
                        global_y = (cy - bounding.bottom) * chunk_width + j
                        pixels[global_x, global_y] = (h, h, h)
    im.save(image_name + '.png')
