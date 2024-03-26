from typing import Optional, Callable, Tuple

from world_map_generator.utils import random_color


def base_height_modification(h: float, biome_parameters: Optional[dict] = None) -> float:
    return h


class BiomeType:
    """ Type of biome instance.

    Attributes:
        title                   The title of the biome type.
        height_modification     Method which will be used to modify heightmap values at this biome type.
        biome_parameters        Dict of some additional parameters (f.e. appearance_weight).
        rendering_color         RGB color which will be used in rendering.
                                If rendering_color is None, the color will be selected randomly.
    """

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
    """ Biome type with specified position.

    Attributes:
        x               Global x position in biome chunks.
        y               Global y position in biome chunks.
        biome_type      Type of current biome.
    """

    def __init__(self, x: float, y: float, biome_type: BiomeType):
        self.x = x
        self.y = y
        self.biome_type = biome_type


BASE_BIOME_TYPE = BiomeType('Base biome')
