from typing import Optional, Callable, Tuple

from src.utils import random_color


def base_height_modification(h: float, biome_parameters: Optional[dict] = None) -> float:
    return h


class BiomeType:

    def __init__(self,
                 title: str,
                 height_modification: Optional[Callable[[float, dict], float]] = base_height_modification,
                 biome_parameters: Optional[dict] = None,
                 rendering_color: Optional[Tuple[int, int, int]] = None):
        if title is None:
            raise Exception("title should be specified!")
        self.title = title
        if height_modification is None:
            raise Exception("height_modification couldn't be None!")
        self.height_modification = height_modification
        if biome_parameters is None:
            self.biome_parameters = {}
        else:
            self.biome_parameters = biome_parameters
        if rendering_color is None:
            self.rendering_color = random_color()
        else:
            self.rendering_color = rendering_color


class BiomeInstance:
    """Chunk with information about bioms types and their weights in tiles.

    Attributes:
        x               Global x position in tiles.
        y               Global y position in tiles.
        biome_type      Type of current biome.
    """

    def __init__(self, x: float, y: float, biome_type: BiomeType):
        self.x = x
        self.y = y
        self.biome_type = biome_type


BASE_BIOME_TYPE = BiomeType('Base biome')
