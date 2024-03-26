# Version
FRACTAL_GENERATOR_VERSION = '0.2.0'

# General generators parameters
TILES_IN_CHUNK = 64

# Fractal map generation
DIAMOND_SQUARE_GRID_STEP = 128
DIAMOND_SQUARE_BASE_GRID_MAX_VALUE = 100

# Biome generation
# BIOME_GRID_STEP:      Distance between biome grid cells.
#                       Near each node will be created biome with central position +- half of grid step.
#                       Biomes area will be calculated with Voronoi algorithm.
BIOME_GRID_STEP = 128
# BIOME_BLEND_RADIOS:   Radios of borders smoothing between biomes.
#                       After smoothing  each point near biome borders will have average nearby biomes
#                       values with weights.
BIOME_BLEND_RADIOS = 15
