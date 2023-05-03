from typing import Optional, Callable, Tuple

from src.utils import random_color


def base_height_modification(h: float, biome_parameters: Optional[dict] = None) -> float:
    return h


class BiomeType:

    def __init__(self,
                 height_modification_method: Optional[Callable[[float, dict], float]] = base_height_modification,
                 biome_parameters: Optional[dict] = None,
                 rendering_color: Optional[Tuple[int, int, int]] = None):
        self.height_modification = height_modification_method
        if biome_parameters is None:
            self.biome_parameters = {}
        else:
            self.biome_parameters = biome_parameters
        if rendering_color is None:
            self.rendering_color = random_color()
        else:
            self.rendering_color = rendering_color


BASE_BIOME_TYPE = BiomeType()
