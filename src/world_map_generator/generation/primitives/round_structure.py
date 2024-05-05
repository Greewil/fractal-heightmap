from typing import Optional, Callable

from numpy import pi, cos

from world_map_generator.default_values import ROUND_STRUCTURE_BASE_MAX_RADIUS, ROUND_STRUCTURE_BASE_MAX_VALUE


def step_radius_function(r: float, max_r: float, max_value: float, parameters: Optional[dict] = None) -> float:
    return max_value


def linear_radius_function(r: float, max_r: float, max_value: float, parameters: Optional[dict] = None) -> float:
    return max_value * (1 - r / max_r)


def cos_radius_function(r: float, max_r: float, max_value: float, parameters: Optional[dict] = None) -> float:
    return max_value * 0.5 * (1 + cos(r * pi / max_r))


def cos_cos_radius_function(r: float, max_r: float, max_value: float, parameters: Optional[dict] = None) -> float:
    cos_r = 0.5 * (1 + cos(r * pi / max_r))
    return max_value * 0.5 * (1 + cos(pi * (1 - cos_r)))


def cos_hyperbole_radius_function(r: float, max_r: float, max_value: float, parameters: Optional[dict] = None) -> float:
    hyperbole_r = (1 - 1 / (1 + r / max_r))
    return max_value * 0.5 * (1 + cos(2 * pi * hyperbole_r))


class RoundStructureType:
    """ Type of round structure instance.

    Attributes:
        title                       The title of the round structure type.
        max_r                       Maximum distance from round structure center
                                    which can be handled due generation.
        max_value                   Maximum value that can be generated with current round structure.
        radius_function             Method which will be used to generate values near this round structure type.
                                    Where input parameters are:
                                        r - distance to round structure center (float),
                                        max_r - max distance from tile to round structure center
                                            which can be handled due generation (float),
                                        parameters - round structure type parameters (dict).
        parameters                  Dict of some additional parameters (f.e. appearance_weight).
    """

    def __init__(self,
                 title: str,
                 max_r: float = ROUND_STRUCTURE_BASE_MAX_RADIUS,
                 max_value: float = ROUND_STRUCTURE_BASE_MAX_VALUE,
                 radius_function: Optional[Callable[[float, float, float, dict], float]] = step_radius_function,
                 parameters: Optional[dict] = None):
        """ Type of round structure instance.
        :param title:                   The title of the round structure type.
        :param max_r:                   Maximum distance from round structure center
                                        which can be handled due generation.
        :param max_value:               Maximum value that can be generated with current round structure.
        :param radius_function:         Method which will be used to generate values near this round structure type.
                                        Where input parameters are:
                                            r - distance to round structure center (float),
                                            max_r - max distance from tile to round structure center
                                                which can be handled due generation (float).
                                            max_value - max value that can be generated
                                                with current round structure (float),
                                            parameters - round structure type parameters (dict).
        :param parameters:              Dict of some additional parameters (f.e. appearance_weight).
        """
        if title is None:
            raise Exception("title should be specified!")
        self.title = title
        self.max_r = max_r
        self.max_value = max_value
        if radius_function is None:
            raise Exception("radius_function couldn't be None!")
        self.radius_function = radius_function
        if parameters is None:
            self.parameters = {}
        else:
            self.parameters = parameters


class RoundStructureInstance:
    """ Round structure type with specified position.

    Attributes:
        x                       Global x position in round structure chunk grid.
        y                       Global y position in round structure chunk grid.
        round_structure_type    Type of current round structure.
    """

    def __init__(self, x: float, y: float, round_structure_type: RoundStructureType):
        """ Round structure type with specified position.
        :param x:                       Global x position in round structure chunk grid.
        :param y:                       Global y position in round structure chunk grid.
        :param round_structure_type:    Type of current round structure.
        """
        self.x = x
        self.y = y
        self.round_structure_type = round_structure_type


STEP_ROUND_STRUCTURE_TYPE = RoundStructureType('Step round structure')
COS_ROUND_STRUCTURE_TYPE = RoundStructureType('Cos round structure', radius_function=cos_radius_function)
COS_COS_ROUND_STRUCTURE_TYPE = RoundStructureType('Cos(cos) round structure', radius_function=cos_cos_radius_function)
COS_HYPERBOLE_ROUND_STRUCTURE_TYPE = RoundStructureType('Cos(hyperbole) round structure',
                                                        radius_function=cos_hyperbole_radius_function)
LINEAR_ROUND_STRUCTURE_TYPE = RoundStructureType('Linear round structure', radius_function=linear_radius_function)
