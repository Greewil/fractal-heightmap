import math
from typing import Optional, List, Tuple, Callable

import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
from scipy.spatial import Voronoi

from world_map_generator.default_values import DEFAULT_CHUNK_WIDTH, DEFAULT_BIOME_GRID_STEP, DEFAULT_BIOME_BLEND_RADIOS
from .chunk_generator import ChunkGenerator
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType, BiomeInstance, BASE_BIOME_TYPE, add_biome_to_biome_tile
from world_map_generator.map.chunk import BiomeChunk
from world_map_generator.utils import Bounding
from world_map_generator.utils import get_position_seed


def get_base_biome_type(biome_node_x: int, biome_node_y: int, seed: int) -> BiomeType:
    return BASE_BIOME_TYPE


class BiomeGenerator(ChunkGenerator):
    """ Generator of biome map chunks based on voronoi algorithm.

    Attributes:
        seed                    Number which is used in procedural generation.
                                If it wasn't specified it will be generated randomly.
        chunk_width             Chunk size which defines tiles matrix.
                                Tile matrix size which should be [chunk_width x chunk_width].
                                Chunk width should be the power of 2.
        biome_grid_step         Distance between two closest base grid biome region centers.
                                Near one biome region center will be created biome center
                                and biome area will be determined with voronoi algorithm.
        biome_blend_radios      Width of biome blending line in which biomes will be mixed together.
        get_biome_type          Method which contains logic about biome type placement on map.
                                First parameter is biome_node_x, second - biome_node_y, third - biome map seed.
                                Method returns BiomeType.
    """

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = DEFAULT_CHUNK_WIDTH,
                 biome_grid_step: Optional[int] = DEFAULT_BIOME_GRID_STEP,
                 biome_blend_radios: Optional[int] = DEFAULT_BIOME_BLEND_RADIOS,
                 get_biome_type: Callable[[int, int, int], BiomeType] = get_base_biome_type):
        """ Generator of biome map chunks based on voronoi algorithm.
        :param seed:                Number which is used in procedural generation.
                                    If it wasn't specified it will be generated randomly.
        :param chunk_width:         Chunk size which defines tiles matrix.
                                    Tile matrix size which should be [chunk_width x chunk_width].
                                    Chunk width should be the power of 2.
        :param biome_grid_step:     Distance between two closest base grid region centers.
                                    Near one region center will be created biome center
                                    and biome area will be determined with voronoi algorithm.
        :param biome_blend_radios:  Width of biome blending line in which biomes will be mixed together.
        :param get_biome_type:      Method which contains logic about biome type placement on map.
                                    First parameter is biome_node_x, second - biome_node_y, third - biome map seed.
                                    Method returns BiomeType.
        """
        super().__init__(seed, chunk_width)
        self._biome_grid_step = biome_grid_step
        self._biome_blend_radios = biome_blend_radios
        self._get_biome_type = get_biome_type
        self._clean_value_matrix()
        self._blending_point_code = 255
        # may be use "RGB" instead of if more than 255 types (1 for borders) of biomes

    @property
    def biome_grid_step(self):
        return self._biome_grid_step

    @property
    def biome_blend_radios(self):
        return self._biome_blend_radios

    @property
    def get_biome_type(self):
        return self._get_biome_type

    def _clean_value_matrix(self):
        """ Sets values of value_matrix (matrix of chunk_width size need for generation) to zeros. """
        self.value_matrix = []
        for i in range(self.chunk_width):
            self.value_matrix.append([])
            for j in range(self.chunk_width):
                self.value_matrix[i].append([])

    def get_closest_biomes_bounding(self, chunk_x: int, chunk_y: int) -> Bounding:
        """
        Returns the bounding for biome instances which are close enough to impact chunk generation
        in specified coordinates.
        """
        biome_grid_left_x = (chunk_x * self.chunk_width // self.biome_grid_step) - 2
        biome_grid_bottom_y = (chunk_y * self.chunk_width // self.biome_grid_step) - 2
        biome_grid_right_x = ((chunk_x + 1) * self.chunk_width // self.biome_grid_step) + 2
        biome_grid_top_y = ((chunk_y + 1) * self.chunk_width // self.biome_grid_step) + 2
        return Bounding(biome_grid_left_x, biome_grid_bottom_y, biome_grid_right_x, biome_grid_top_y)

    def get_biome_center(self, biome_node_x: int, biome_node_y: int) -> Tuple[float, float]:
        """ Returns position of biome center which will be the center of voronoi cell. """
        pos_seed = get_position_seed(biome_node_x, biome_node_y, self.seed)
        np.random.seed(pos_seed)
        rnd = np.random.rand(2)
        biome_center_x = self.biome_grid_step * (biome_node_x + rnd[0] - 0.5)
        biome_center_y = self.biome_grid_step * (biome_node_y + rnd[1] - 0.5)
        return biome_center_x, biome_center_y

    def get_closest_biomes(self, chunk_x: int, chunk_y: int) -> List[BiomeInstance]:
        """ Returns list of biome instances which are close enough to impact chunk generation. """
        biome_grid_bounding = self.get_closest_biomes_bounding(chunk_x, chunk_y)
        biomes = []
        for i in range(biome_grid_bounding.left, biome_grid_bounding.right + 1):
            for j in range(biome_grid_bounding.bottom, biome_grid_bounding.top + 1):
                biome_center = self.get_biome_center(i, j)
                biome_type = self.get_biome_type(i, j, self.seed)
                biome_instance = BiomeInstance(biome_center[0], biome_center[1], biome_type)
                biomes.append(biome_instance)
        return biomes

    def _get_closest_biomes_mix(self, tile_x: int, tile_y: int,
                                biomes: List[BiomeInstance]) -> List[Tuple[float, BiomeType]]:
        """ Returns biomes mix which contains only biome which center is closest to specified tile. """
        min_dist = 5 * self.biome_grid_step * self.biome_grid_step
        closest_biome_id = 0
        biome_distances = np.full(len(biomes), 0.0)
        for i in range(len(biomes)):
            dx, dy = tile_x - biomes[i].x, tile_y - biomes[i].y
            cur_distance = dx * dx + dy * dy
            biome_distances[i] = cur_distance
            if cur_distance < min_dist:
                min_dist = cur_distance
                closest_biome_id = i
        return [(1, biomes[closest_biome_id].biome_type)]

    def generate_chunk_of_values_slow(self, chunk_x: int, chunk_y: int,
                                      closest_biomes: List[BiomeInstance]) -> BiomeChunk:
        """
        Slow way to generate a chunk of values for biome map

        :param chunk_x: chunk x position in world
        :param chunk_y: chunk y position in world
        :param closest_biomes: list of closest biome instances
        :return: numpy matrix with size = [chunk_width x chunk_width]
        """
        self._clean_value_matrix()
        output_chunk_left = self.chunk_width * chunk_x
        output_chunk_bottom = self.chunk_width * chunk_y

        for i in range(self.chunk_width):
            for j in range(self.chunk_width):
                x, y = i + output_chunk_left, j + output_chunk_bottom
                biomes_mix = self._get_closest_biomes_mix(x, y, closest_biomes)
                self.value_matrix[i][j] = biomes_mix

        output_chunk = BiomeChunk(chunk_x, chunk_y, self.chunk_width, self.value_matrix)
        return output_chunk

    def _get_central_points(self, closest_biomes: List[BiomeInstance],
                            output_chunk_left: int,
                            output_chunk_bottom: int):
        """ Returns numpy array of 2d points of centers of all biome instances 4 plus bounding points."""
        central_points = np.array([[x.x - output_chunk_left + self.biome_blend_radios,
                                    x.y - output_chunk_bottom + self.biome_blend_radios] for x in closest_biomes])
        central_points = np.append(central_points, [[-8 * self.biome_grid_step, 0.5 * self.chunk_width],
                                                    [8 * self.biome_grid_step, 0.5 * self.chunk_width],
                                                    [0.5 * self.chunk_width, -8 * self.biome_grid_step],
                                                    [0.5 * self.chunk_width, 8 * self.biome_grid_step]], axis=0)
        return central_points

    def _draw_voronoi(self, central_points, borders_smoothing: bool = False) -> Tuple[np.array, np.array]:
        """
        Rendering images of voronoi regions (basic and bordered) with use of PIL library
        and converts them to numpy arrays.
        Values of the regions corresponds to indices of central points.
        Value 255 stands for borders.
        Sizes of both images are equals to (chunk_width + 2 * biome_blend_radios).

        :param central_points: array of voronoi region's central points.
        :param borders_smoothing: if its True method also generates image with bordered voronoi regions
        :return: tuple with two images as numpy arrays (image of voronoi regions, image of bordered voronoi regions)
        """
        vor = Voronoi(central_points)
        vertices = vor.vertices

        voronoi_image_size = self.chunk_width + 2 * self.biome_blend_radios
        voronoi_image = Image.new("L", (voronoi_image_size, voronoi_image_size), self._blending_point_code)
        voronoi_bordered_image = Image.new("L", (voronoi_image_size, voronoi_image_size), self._blending_point_code)

        voronoi_draw = ImageDraw.Draw(voronoi_image)
        voronoi_bordered_draw = ImageDraw.Draw(voronoi_bordered_image)

        for i in range(len(vor.point_region)):
            cur_region = vor.regions[vor.point_region[i]]

            cur_polygon = []
            bad_region = False
            for j in cur_region:
                if j == -1:
                    bad_region = True
                    break
                cur_polygon.append((vertices[j][0], vertices[j][1]))

            if not bad_region:
                cur_polygon = tuple(cur_polygon)
                voronoi_draw.polygon(xy=cur_polygon, fill=i)
                if borders_smoothing:
                    voronoi_bordered_draw.polygon(xy=cur_polygon,
                                                  fill=i,
                                                  outline=self._blending_point_code,
                                                  width=int(0.5 * self.biome_blend_radios))
        return np.array(voronoi_image), np.array(voronoi_bordered_image)

    def generate_chunk_fast_voronoi(self, chunk_x: int, chunk_y: int,
                                    closest_biomes: List[BiomeInstance],
                                    value_maps: List[Map] = None) -> BiomeChunk:
        """
        Biome chunk generation

        :param value_maps: list of Map instances which would be used for biome generation (min 1 additional map)
        :param chunk_x: chunk x position in world
        :param chunk_y: chunk y position in world
        :param closest_biomes: list of biome instances which are close enough to impact chunk generation.
        :return: numpy matrix with size = [chunk_width x chunk_width]
        """
        self._clean_value_matrix()
        output_chunk_left = self.chunk_width * chunk_x
        output_chunk_bottom = self.chunk_width * chunk_y
        central_points = self._get_central_points(closest_biomes, output_chunk_left, output_chunk_bottom)

        additional_values = None
        if value_maps is not None:
            additional_values = []
            for vm in value_maps:
                additional_values.append(vm.get_chunk(chunk_x, chunk_y).tiles)
            shift_map_x = value_maps[0].get_chunk(chunk_x, chunk_y).tiles
            shift_map_y = value_maps[0].get_chunk(chunk_x + 1, chunk_y).tiles
        borders_smoothing = True
        if additional_values is None or self.biome_blend_radios == 0:
            borders_smoothing = False

        self._blending_point_code = 255

        np_voronoi_image, np_voronoi_bordered_image = self._draw_voronoi(central_points, borders_smoothing)

        for i in range(self.biome_blend_radios, self.chunk_width + self.biome_blend_radios):
            for j in range(self.biome_blend_radios, self.chunk_width + self.biome_blend_radios):
                cur_biome_not_blended_id = np_voronoi_image[j, i]
                in_chunk_x, in_chunk_y = i - self.biome_blend_radios, j - self.biome_blend_radios
                weighted_biomes = self.value_matrix[i - self.biome_blend_radios][j - self.biome_blend_radios]
                if not borders_smoothing:
                    weighted_biome_type = (1, closest_biomes[cur_biome_not_blended_id].biome_type)
                    add_biome_to_biome_tile(weighted_biomes, weighted_biome_type)
                else:
                    shift_x = int(self.biome_blend_radios * (shift_map_x[in_chunk_x, in_chunk_y] - 0.5))
                    shift_y = int(self.biome_blend_radios * (shift_map_y[in_chunk_x, in_chunk_y] - 0.5))
                    cur_biome_blended_id = np_voronoi_image[j + shift_x, i + shift_y]
                    cur_biome_not_blended_id = np_voronoi_bordered_image[j + shift_x, i + shift_y]
                    if cur_biome_not_blended_id != self._blending_point_code:
                        weighted_biome_type = (shift_map_x[in_chunk_x, in_chunk_y],
                                               closest_biomes[cur_biome_not_blended_id].biome_type)
                        add_biome_to_biome_tile(weighted_biomes, weighted_biome_type)
                    else:
                        weighted_biome_type = (1, closest_biomes[cur_biome_blended_id].biome_type)
                        add_biome_to_biome_tile(weighted_biomes, weighted_biome_type)
                        # maybe use few random point and then little smooth
                        for n in range(int(1.5 * self.biome_blend_radios)):
                            rnd = np.random.rand(2)
                            dx = int(self.biome_blend_radios * (rnd[0] - 0.5))
                            dy = int(self.biome_blend_radios * (rnd[1] - 0.5))
                            additional_biome_id = np_voronoi_image[j + dx + shift_x, i + dy + shift_y]
                            # if cur_biome_blended_id != additional_biome_id:
                            if dx != 0 or dy != 0:
                                blend_weight = 1 / math.sqrt(dx * dx + dy * dy)
                                weighted_biome_type = (blend_weight, closest_biomes[additional_biome_id].biome_type)
                                add_biome_to_biome_tile(weighted_biomes, weighted_biome_type)

        output_chunk = BiomeChunk(chunk_x, chunk_y, self.chunk_width, self.value_matrix)
        return output_chunk

    def generate_chunk(self, chunk_x: int, chunk_y: int, value_maps: List[Map] = None) -> BiomeChunk:
        """
        Biome chunk generation

        :param value_maps: list of Map instances which would be used for biome generation (min 1 additional map)
        :param chunk_x: chunk x position in world
        :param chunk_y: chunk y position in world
        :return: biome chunk with size = [chunk_width x chunk_width]
        """
        closest_biomes = self.get_closest_biomes(chunk_x, chunk_y)
        return self.generate_chunk_fast_voronoi(chunk_x, chunk_y, closest_biomes, value_maps)
