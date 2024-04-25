from typing import Optional, Callable, Tuple, List

from world_map_generator.utils import random_color


def base_height_modification(h: float,
                             biome_parameters: Optional[dict] = None,
                             value_maps_values: Optional[List[float]] = None) -> float:
    return h


class BiomeType:
    """ Type of biome instance.

    Attributes:
        title                   The title of the biome type.
        height_modification     Method which will be used to modify heightmap values at this biome type.
                                Where first input parameter is height to modify, second - biome_parameters,
                                third - list of additional value_map values for current tile which will be
                                modified.
        biome_parameters        Dict of some additional parameters (f.e. appearance_weight).
        rendering_color         RGB color which will be used in rendering.
                                If rendering_color is None, the color will be selected randomly.
    """

    def __init__(self,
                 title: str,
                 height_modification: Optional[Callable[[float, dict, List[float]], float]] = base_height_modification,
                 biome_parameters: Optional[dict] = None,
                 rendering_color: Optional[Tuple[int, int, int]] = None):
        """ Type of biome instance.
        :param title:                   The title of the biome type.
        :param height_modification:     Method which will be used to modify heightmap values at this biome type.
                                        Where first input parameter is height to modify, second - biome_parameters,
                                        third - list of additional value_map values for current tile which will be
                                        modified.
        :param biome_parameters:        Dict of some additional parameters (f.e. appearance_weight).
        :param rendering_color:         RGB color which will be used in rendering.
                                        If rendering_color is None, the color will be selected randomly.
        """
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
        x               Global x position in biome chunk grid.
        y               Global y position in biome chunk grid.
        biome_type      Type of current biome.
    """

    def __init__(self, x: float, y: float, biome_type: BiomeType):
        """ Biome type with specified position.
        :param x:               Global x position in biome chunk grid.
        :param y:               Global y position in biome chunk grid.
        :param biome_type:      Type of current biome.
        """
        self.x = x
        self.y = y
        self.biome_type = biome_type


BASE_BIOME_TYPE = BiomeType('Base biome')
