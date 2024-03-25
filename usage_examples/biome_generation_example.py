import functools
import time

from world_map_generator.generation import BiomeGenerator, FractalGenerator
from world_map_generator.map import Map
from world_map_generator.map.biome import BiomeType
from world_map_generator.map.chunk import ValueChunk
from world_map_generator.rendering import save_biome_map_as_image, save_height_map_as_image
from world_map_generator.utils import get_position_seed, weighted_random_selection, get_cumulative_distribution_list, \
    Bounding

biome_example_1 = BiomeType(title='biome 1', biome_parameters={'appearance_weight': 2})
biome_example_2 = BiomeType(title='biome 2', biome_parameters={'appearance_weight': 1})
biome_example_3 = BiomeType(title='biome 3', biome_parameters={'appearance_weight': 1})
biome_types_pool = [biome_example_1, biome_example_2]
# biome_types_pool = [biome_example_1, biome_example_2, biome_example_3]
biomes_weights = [b.biome_parameters['appearance_weight'] for b in biome_types_pool]
biomes_cumulative_distribution = get_cumulative_distribution_list(biomes_weights)


@functools.lru_cache(maxsize=1000, typed=False)
def get_random_biome_example(biome_node_x: int, biome_node_y: int, seed: int) -> BiomeType:
    pos_seed = get_position_seed(biome_node_x, biome_node_y, seed + 69)
    biome_index = weighted_random_selection(biomes_cumulative_distribution, pos_seed)
    return biome_types_pool[biome_index]


if __name__ == '__main__':
    # chunk_width = 16
    chunk_width = 32
    # chunk_width = 64

    base_grid_distance = chunk_width
    base_grid_max_value = 1

    biome_grid_step = 128
    biome_blend_radios = 20

    seed = 42

    # bounding = Bounding(-5, -5, 6, 6)
    bounding = Bounding(-10, -10, 10, 10)
    # bounding = Bounding(-20, -20, 20, 20)
    # bounding = Bounding(5, -6, 6, -4)
    # bounding = Bounding(-5, -5, 0, 0)
    # bounding = Bounding(-1, -1, 0, 0)

    biome_map = Map(seed, chunk_width=chunk_width)

    biome_generator = BiomeGenerator(biome_map.seed, chunk_width, biome_grid_step, biome_blend_radios)

    # print(f'seed = {biome_map.seed}')
    # start = time.process_time()
    # for i in range(bounding.left, bounding.right):
    #     for j in range(bounding.bottom, bounding.top):
    #         closest_biomes = biome_generator.get_closes_biomes(i, j, get_random_biome_example)
    #         print(i, j, len(closest_biomes), 'closest_biomes')
    #         chunk = biome_generator.generate_chunk_of_values(i, j, closest_biomes)
    #         biome_map.set_chunk(chunk)
    # print(time.process_time() - start, 'seconds')
    # print(biome_map.number_of_generated_chunks(), biome_map.number_of_generated_tiles())
    # save_biome_map_as_image(biome_map, 'tst_biomes')

    shift_map = Map(seed + 1, chunk_width=chunk_width)
    shift_generator = FractalGenerator(shift_map.seed, chunk_width, base_grid_distance, base_grid_max_value)
    start = time.process_time()
    wider_bounding = Bounding(0, 0, 1, 0)
    wider_bounding.add_bounding(bounding)
    wider_bounding.for_each(lambda x, y:
                            shift_map.set_chunk(ValueChunk(x, y, tiles=shift_generator.generate_chunk_of_values(x, y))))
    print(time.process_time() - start, 'seconds', '(shift_map)')
    save_height_map_as_image(shift_map, 'shift_map', max_color_value=1.5 * base_grid_max_value)

    def generate_biomes_chunk(x: int, y: int):
        closest_biomes = biome_generator.get_closes_biomes(x, y, get_random_biome_example)
        print(x, y, len(closest_biomes), 'closest_biomes')

        chunk = biome_generator.generate_chunk_of_values_fast_voronoi(x, y, closest_biomes, [shift_map])
        biome_map.set_chunk(chunk)

    start = time.process_time()
    bounding.for_each(generate_biomes_chunk)
    print(time.process_time() - start, 'seconds')
    print(biome_map.number_of_generated_chunks(), biome_map.number_of_generated_tiles())
    save_biome_map_as_image(biome_map, 'tst_biomes')
