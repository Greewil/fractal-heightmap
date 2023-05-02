from typing import Optional, List

import numpy as np

from new_src.default_values import *
from new_src.map.map import Map
from new_src.utils import Bounding
from new_src.utils import get_position_seed, is_power_of_two


class FractalGenerator:

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = TILES_IN_CHUNK,
                 base_grid_distance: Optional[int] = DIAMOND_SQUARE_GRID_DISTANCE) -> None:
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

        # self.x_start = 0
        # self.y_start = 0
        # self.lefter_chunk = 0
        # self.bottom_chunk = 0
        # self.border_size = 2 * self.base_grid_distance + self.chunk_width
        # self.current_size = 2 * self.border_size + self.chunk_width
        # self.current_size_chunks = self.current_size // self.chunk_width
        # self.border_size_chunks = self.border_size // self.chunk_width

        self.chunks_in_base_grid_step = self.base_grid_distance // self.chunk_width
        # if self.chunk_width > self.base_grid_distance:
        #     self.value_matrix_width_chunks = 3  # 1 +- 1
        # else:
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
    def chunk_width(self):
        return self._chunk_width

    @property
    def base_grid_steps(self):
        return self._base_grid_steps

    @property
    def base_grid_distance(self):
        return self._base_grid_distance

    def _get_chunks_bounding(self, chunk_x: int, chunk_y: int) -> Bounding:
        grid_corner_x = chunk_x % self.chunks_in_base_grid_step
        grid_corner_y = chunk_y % self.chunks_in_base_grid_step
        return Bounding(chunk_x - grid_corner_x - self.chunks_in_base_grid_step,
                        chunk_y - grid_corner_y - self.chunks_in_base_grid_step,
                        chunk_x - grid_corner_x + 3 * self.chunks_in_base_grid_step,
                        chunk_y - grid_corner_y + 3 * self.chunks_in_base_grid_step)

    def _generate_random_sequence(self, bounding: Bounding):
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
        self.value_matrix = np.full((self.value_matrix_width_tiles, self.value_matrix_width_tiles), 0.0)

    def _generate_base_grid(self):
        for i in range(self.value_matrix_width_tiles // self.base_grid_distance):
            for j in range(self.value_matrix_width_tiles // self.base_grid_distance):
                x = i * self.base_grid_distance
                y = j * self.base_grid_distance
                self.value_matrix[x, y] = self._random_sequence[x, y] * 100

    def _diamond_square_step(self, step, target_left: int, target_bottom: int, target_right: int, target_top: int):
        step_size = 2 ** step
        step_size_double = 2 * step_size
        radii = self.steps_impact_radii[step]
        # x-shape step
        cur_x = step_size
        max_step_random = 100 / 2 ** (self.base_grid_steps - step - 1)
        while cur_x <= target_right + radii[1]:
            cur_y = step_size
            while cur_y <= target_top + radii[1]:
                self.value_matrix[cur_x, cur_y] = 0.25 * (self.value_matrix[cur_x - step_size, cur_y - step_size] +
                                                          self.value_matrix[cur_x - step_size, cur_y + step_size] +
                                                          self.value_matrix[cur_x + step_size, cur_y - step_size] +
                                                          self.value_matrix[cur_x + step_size, cur_y + step_size]) + \
                                                  (self._random_sequence[cur_x, cur_y] - 0.5) * max_step_random
                cur_y += step_size_double
            cur_x += step_size_double
        # +-shape step
        cur_x = step_size
        i = 1
        max_step_random = max_step_random * 0.25
        while cur_x <= target_right + radii[0]:
            cur_y = step_size + (i % 2) * step_size
            while cur_y <= target_top + radii[0]:
                self.value_matrix[cur_x, cur_y] = 0.25 * (self.value_matrix[cur_x + step_size, cur_y] +
                                                          self.value_matrix[cur_x - step_size, cur_y] +
                                                          self.value_matrix[cur_x, cur_y - step_size] +
                                                          self.value_matrix[cur_x, cur_y + step_size]) + \
                                                  (self._random_sequence[cur_x, cur_y] - 0.5) * max_step_random
                cur_y += step_size_double
            cur_x += step_size
            i += 1

    def generate_chunk_of_values(self, chunk_x: int, chunk_y: int):
        """
        Fractal chunk generation
        :param chunk_x: chunk x position in world
        :param chunk_y: chunk y position in world
        :return: numpy matrix with size = chunk_width x chunk_width
        """
        chunks_bounding = self._get_chunks_bounding(chunk_x, chunk_y)
        self._generate_random_sequence(chunks_bounding)
        self._clean_value_matrix()
        self._generate_base_grid()
        output_chunk_left = self.base_grid_distance + self.chunk_width * (chunk_x % self.chunks_in_base_grid_step)
        output_chunk_bottom = self.base_grid_distance + self.chunk_width * (chunk_y % self.chunks_in_base_grid_step)
        output_chunk_right = output_chunk_left + self.chunk_width
        output_chunk_top = output_chunk_bottom + self.chunk_width
        # print(chunks_bounding, output_chunk_left, output_chunk_right)

        for step in range(self.base_grid_steps - 1, -1, -1):
            self._diamond_square_step(step,
                                      output_chunk_left, output_chunk_bottom,
                                      output_chunk_right, output_chunk_top)
        # x_start = chunk_x * self.tiles_in_chunk
        # y_start = chunk_y * self.tiles_in_chunk
        # self.lefter_chunk = chunk_x - self.border_size_chunks
        # self.bottom_chunk = chunk_y - self.border_size_chunks
        # filling with values according to algorithm
        # for i in range(self.border_size, self.border_size + self.tiles_in_chunk):
        #     for j in range(self.border_size, self.border_size + self.tiles_in_chunk):
        #         x = i + x_start
        #         y = j + y_start
        #         self.current_values[i][j] = self._get_diamond_square_result(x, y, self.map.seed)[0]
        # generating output chunk of values:
        chunk = self.value_matrix[output_chunk_left:output_chunk_right, output_chunk_bottom:output_chunk_top]
        return chunk

    # def _get_diamond_square_result(self, x: int, y: int, seed: int) -> Tuple[float]:
    #     """Uses diamond_square algorithm to recursively generate values ranges in point
    #     return [0] - value, [1] - range"""
    #     step_size = 0
    #     state = None
    #     loc_x = 0
    #     loc_y = 0
    #     rnd_ind = 0
    #     dv_multipliar = 0
    #     value = 0
    #     diamond_square_range = 0
    #     if self._is_local_value_exists(x, y):
    #         value = self._get_local_value(x, y)
    #         diamond_square_range = self._get_local_step(x, y)
    #         return (value, diamond_square_range)
    #     else:
    #         step = 1
    #         for i in range(DIAMOND_SQUARE_GRID_STEPS, 0, -1):
    #             step_size = 2 ** i
    #             if (x % step_size == 0) and (y % step_size == 0):
    #                 step = step_size
    #                 break
    #         if (step == 2 ** DIAMOND_SQUARE_GRID_STEPS):
    #             reference_point_info = self.get_reference_point_info(x, y, self.closest_biomes)
    #             self._set_local_value(x, y, reference_point_info[0])
    #             self._set_local_step(x, y, reference_point_info[1])
    #             return reference_point_info
    #         else:
    #             average_value = 0
    #             average_step = 0
    #             if (x % (step * 2) == 0) or (y % (step * 2) == 0):
    #                 v1, st1 = self._get_diamond_square_result(x - step, y, seed)
    #                 v2, st2 = self._get_diamond_square_result(x + step, y, seed)
    #                 v3, st3 = self._get_diamond_square_result(x, y - step, seed)
    #                 v4, st4 = self._get_diamond_square_result(x, y + step, seed)
    #             else:
    #                 v1, st1 = self._get_diamond_square_result(x - step, y - step, seed)
    #                 v2, st2 = self._get_diamond_square_result(x - step, y + step, seed)
    #                 v3, st3 = self._get_diamond_square_result(x + step, y - step, seed)
    #                 v4, st4 = self._get_diamond_square_result(x + step, y + step, seed)
    #             average_value += v1 + v2 + v3 + v4
    #             average_step += st1 + st2 + st3 + st4
    #             # print(x//self.tiles_in_chunk - self.lefter_chunk, y//self.tiles_in_chunk - self.bottom_chunk, self.lefter_chunk, self.bottom_chunk)
    #             diamond_square_range = average_step / 4 * step / 18
    #             state = self.random_states[x // self.tiles_in_chunk - self.lefter_chunk - 1][
    #                 y // self.tiles_in_chunk - self.bottom_chunk - 1]
    #             loc_x = (x - self.x_start) % self.tiles_in_chunk
    #             loc_y = (y - self.y_start) % self.tiles_in_chunk
    #             rnd_ind = loc_x * self.tiles_in_chunk + loc_y
    #             dv_multipliar = state[rnd_ind % RANDOM_STATE_STACK_SIZE] / MAX_RANDOM_STATE_CHUNK
    #             dv_multipliar = diamond_square_range * (dv_multipliar - 0.5)
    #             # dv_multipliar = random_from_seed_in_range(-1.0*step/2, 1.0*step/2, random_from_seed(seed + x) + y)
    #             value = self._averaging(average_value / 4, dv_multipliar)
    #             self._set_local_value(x, y, value)
    #             self._set_local_step(x, y, diamond_square_range)
    #             return (value, diamond_square_range)
    #
    # def _averaging(self, average: float, dv_multipliar: float) -> float:
    #     return average + dv_multipliar
