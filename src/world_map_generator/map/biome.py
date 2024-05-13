from typing import Optional, Callable, Tuple, List

from world_map_generator.utils import random_color


def base_height_modification(height: float,
                             x: int,
                             y: int,
                             seed: int,
                             biome_parameters: Optional[dict] = None,
                             value_maps_values: Optional[List[float]] = None) -> float:
    return height


class BiomeType:
    """ Type of biome instance.

    Attributes:
        title                   The title of the biome type.
        height_modification     Method which will be used to modify heightmap values at this biome type.
                                Where input parameters are:
                                    height - height to modify (float),
                                    x - tile x (int),
                                    y - tile y (int),
                                    seed - map modifier's seed (int),
                                    biome_parameters - dict of biome parameters (dict),
                                    value_maps_values - list of additional value_map values for current tile (list).
        biome_parameters        Dict of some additional parameters (f.e. appearance_weight).
        rendering_color         RGB color which will be used in rendering.
                                If rendering_color is None, the color will be selected randomly.
    """

    def __init__(self,
                 title: str,
                 height_modification: Optional[Callable[[float, int, int, int, dict, List[float]], float]]
                 = base_height_modification,
                 biome_parameters: Optional[dict] = None,
                 rendering_color: Optional[Tuple[int, int, int]] = None):
        """ Type of biome instance.
        :param title:                   The title of the biome type.
        :param height_modification:     Method which will be used to modify heightmap values at this biome type.
                                        Where input parameters are:
                                            height - height to modify (float),
                                            x - tile x (int),
                                            y - tile y (int),
                                            seed - map modifier's seed (int),
                                            biome_parameters - dict of biome parameters (dict),
                                            value_maps_values - list of additional value_map values for current tile
                                                                (list).
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


def is_biome_tiles_same(biome_tile_1: List[Tuple[float, BiomeType]],
                        biome_tile_2: List[Tuple[float, BiomeType]]) -> bool:
    """ Checks if biome tiles are the same (have the same titles and parameters). """
    if (biome_tile_1.title == biome_tile_2.title
            and biome_tile_1.biome_parameters == biome_tile_2.biome_parameters):
        return True
    else:
        return False


def add_biome_to_biome_tile(biome_tile: List[Tuple[float, BiomeType]], weighted_biome_tile: Tuple[float, BiomeType]):
    """
    Adds new tuple if biome tile don't have same biome types yet (with same titles and parameters),
    otherwise adds weight of new tile to weight of same biome type.
    """
    is_collisions = False
    for i in range(len(biome_tile)):
        weight, biome_type = biome_tile[i]
        if is_biome_tiles_same(biome_type, weighted_biome_tile[1]):
            biome_tile[i] = (weighted_biome_tile[0] + weight, biome_type)
            is_collisions = True
            break
    if not is_collisions:
        biome_tile.append(weighted_biome_tile)


def biome_tile_to_dict(biome_tile: List[Tuple[float, BiomeType]]) -> dict:
    output = {}
    for biome in biome_tile:
        output[biome[1].title] = biome[0]
    # TODO save parameters
    # if len(biome_tile) > 1:
    #     print(len(biome_tile), biome_tile)
    #     print(output)
    return output


def dict_to_biome_tile(biome_tile_as_dict: dict, biomes_list: List[BiomeType]) -> List[Tuple[float, BiomeType]]:
    """
    Converts biome tile represented as dictionary to biome tile structure (list of tuples with weights and biome types).

    :param biome_tile_as_dict: Biome tile represented as dictionary.
    :param biomes_list: List of all possible biome types used in map (in case if map filled with BiomeChunks).
    :return: biome tile structure (list of tuples with weights and biome types).
    """
    output = []
    for biome_type_title, weight in biome_tile_as_dict.items():
        biome_type = next((b for b in biomes_list if b.title == biome_type_title), None)
        if biome_type is None:
            raise Exception(f"Biome type {biome_type_title} not found in biomes_list")
        add_biome_to_biome_tile(output, (weight, biome_type))
    return output


BASE_BIOME_TYPE = BiomeType('Base biome')
