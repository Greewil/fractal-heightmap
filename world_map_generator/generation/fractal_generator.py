import math
from typing import Optional

import numpy as np

from world_map_generator.default_values import TILES_IN_CHUNK, DIAMOND_SQUARE_GRID_STEP, \
    DIAMOND_SQUARE_BASE_GRID_MAX_VALUE
from world_map_generator.utils import Bounding, get_random_seed
from world_map_generator.utils import get_position_seed, is_power_of_two


class FractalGenerator:

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = TILES_IN_CHUNK,
                 base_grid_distance: Optional[int] = DIAMOND_SQUARE_GRID_STEP,
                 base_grid_max_value: Optional[float] = DIAMOND_SQUARE_BASE_GRID_MAX_VALUE) -> None:
        if seed is None:
            self.seed = get_random_seed()
        else:
            self.seed = seed
        if not is_power_of_two(chunk_width):
            raise Exception("chunk_width should be the power of 2!")
        if not is_power_of_two(base_grid_distance):
            raise Exception("base_grid_distance should be the power of 2!")
        if base_grid_distance < chunk_width:
            raise Exception("base_grid_distance shouldn't be smaller than chunk_width!")
        self._chunk_width = chunk_width
        self._base_grid_distance = base_grid_distance
        self._base_grid_steps = int(np.log2(base_grid_distance))
        self._base_grid_max_value = base_grid_max_value

        self.chunks_in_base_grid_step = self.base_grid_distance // self.chunk_width
        self.value_matrix_width_chunks = 4 * (self.base_grid_distance // self.chunk_width)
        self.value_matrix_width_tiles = self.value_matrix_width_chunks * self.chunk_width
        self.steps_impact_radii = [(0, 1)]
        additional_value = 1
        for i in range(1, self.base_grid_steps):
            radii = self.steps_impact_radii[i - 1][1] + additional_value
            additional_value *= 2
            self.steps_impact_radii.append((radii, radii + additional_value))
        print(self.steps_impact_radii)
        self._clean_value_matrix()

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value: int):
        self._seed = value % (2 ** 32)

    @property
    def chunk_width(self):
        return self._chunk_width

    @property
    def base_grid_steps(self):
        return self._base_grid_steps

    @property
    def base_grid_distance(self):
        return self._base_grid_distance

    @property
    def base_grid_max_value(self):
        return self._base_grid_max_value

    def _get_chunks_bounding(self, chunk_x: int, chunk_y: int) -> Bounding:
        """ TODO """
        grid_corner_x = chunk_x % self.chunks_in_base_grid_step
        grid_corner_y = chunk_y % self.chunks_in_base_grid_step
        return Bounding(chunk_x - grid_corner_x - self.chunks_in_base_grid_step,
                        chunk_y - grid_corner_y - self.chunks_in_base_grid_step,
                        chunk_x - grid_corner_x + 3 * self.chunks_in_base_grid_step,
                        chunk_y - grid_corner_y + 3 * self.chunks_in_base_grid_step)

    def _generate_random_sequence(self, bounding: Bounding):
        """ TODO """
        randoms_matrix = []
        i = 0
        for x in range(bounding.left, bounding.right + 1):
            randoms_matrix.append([])
            for y in range(bounding.bottom, bounding.top + 1):
                pos_seed = get_position_seed(x, y, self.seed)
                np.random.seed(pos_seed)
                randoms_matrix[i].append(np.random.rand(self.chunk_width, self.chunk_width))
            i += 1
        self._random_sequence = np.bmat(randoms_matrix)

    def _clean_value_matrix(self):
        """ TODO """
        self.value_matrix = np.full((self.value_matrix_width_tiles, self.value_matrix_width_tiles), 0.0)

    def _generate_base_grid(self):
        """ TODO """
        for i in range(self.value_matrix_width_tiles // self.base_grid_distance):
            for j in range(self.value_matrix_width_tiles // self.base_grid_distance):
                x = i * self.base_grid_distance
                y = j * self.base_grid_distance
                self.value_matrix[x, y] = self._random_sequence[x, y] * self.base_grid_max_value

    def _diamond_square_step(self, step, target_left: int, target_bottom: int, target_right: int, target_top: int):
        """ TODO """
        step_size = 2 ** step
        step_size_double = 2 * step_size
        radii = self.steps_impact_radii[step]

        # x-shape step
        cur_x = max(min(step_size + (target_left - radii[1]) // step_size_double * step_size_double,
                        target_bottom),
                    step_size)
        y_start = max(min(step_size + (target_bottom - radii[1]) // step_size_double * step_size_double,
                          target_bottom),
                      step_size)
        max_step_random = self.base_grid_max_value / 2 ** (self.base_grid_steps - step)
        while cur_x <= target_right + radii[1]:
            cur_y = y_start
            while cur_y <= target_top + radii[1]:
                self.value_matrix[cur_x, cur_y] = 0.25 * (self.value_matrix[cur_x - step_size, cur_y - step_size]
                                                          + self.value_matrix[cur_x - step_size, cur_y + step_size]
                                                          + self.value_matrix[cur_x + step_size, cur_y - step_size]
                                                          + self.value_matrix[cur_x + step_size, cur_y + step_size])
                self.value_matrix[cur_x, cur_y] += (self._random_sequence[cur_x, cur_y] - 0.5) * max_step_random
                cur_y += step_size_double
            cur_x += step_size_double

        # +-shape step
        cur_x = min(step_size + (target_left - radii[0]) // step_size_double * step_size_double,
                    target_left)
        y_start = min(step_size + (target_bottom - radii[0]) // step_size_double * step_size_double,
                      target_bottom)
        i = 1
        max_step_random = max_step_random / math.sqrt(2)
        while cur_x <= target_right + radii[0]:
            cur_y = y_start + (i % 2) * step_size
            while cur_y <= target_top + radii[0]:
                self.value_matrix[cur_x, cur_y] = 0.25 * (self.value_matrix[cur_x + step_size, cur_y]
                                                          + self.value_matrix[cur_x - step_size, cur_y]
                                                          + self.value_matrix[cur_x, cur_y - step_size]
                                                          + self.value_matrix[cur_x, cur_y + step_size])
                self.value_matrix[cur_x, cur_y] += (self._random_sequence[cur_x, cur_y] - 0.5) * max_step_random
                cur_y += step_size_double
            cur_x += step_size
            i += 1

    def generate_chunk_of_values(self, chunk_x: int, chunk_y: int):
        """
        Fractal chunk generation
        :param chunk_x: chunk x position in world
        :param chunk_y: chunk y position in world
        :return: numpy matrix with size = [chunk_width x chunk_width]
        """
        chunks_bounding = self._get_chunks_bounding(chunk_x, chunk_y)
        self._generate_random_sequence(chunks_bounding)
        self._clean_value_matrix()
        self._generate_base_grid()
        output_chunk_left = self.base_grid_distance + self.chunk_width * (chunk_x % self.chunks_in_base_grid_step)
        output_chunk_bottom = self.base_grid_distance + self.chunk_width * (chunk_y % self.chunks_in_base_grid_step)
        output_chunk_right = output_chunk_left + self.chunk_width
        output_chunk_top = output_chunk_bottom + self.chunk_width

        for step in range(self.base_grid_steps - 1, -1, -1):
            self._diamond_square_step(step,
                                      output_chunk_left, output_chunk_bottom,
                                      output_chunk_right, output_chunk_top)

        ountput_matrix = self.value_matrix[output_chunk_left:output_chunk_right, output_chunk_bottom:output_chunk_top]
        return ountput_matrix
