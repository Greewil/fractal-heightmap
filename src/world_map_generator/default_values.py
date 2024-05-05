# Version
GENERATOR_VERSION = '0.3.0'

# General generators parameters
TILES_IN_CHUNK = 64

# Fractal map generation
DIAMOND_SQUARE_GRID_STEP = 64
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

# Round structures generation
# ROUND_STRUCTURE_GRID_STEP:        Distance between round structure grid cells.
#                                   Near each node will be created round structure with central
#                                   position +- half of grid step.
ROUND_STRUCTURE_GRID_STEP = 64
# ROUND_STRUCTURE_BASE_MAX_RADIUS:  Maximum distance from round structure center
#                                   which can be handled due generation.
ROUND_STRUCTURE_BASE_MAX_RADIUS = 100
# ROUND_STRUCTURE_BASE_MAX_VALUE:  Maximum value that can be generated with current round structure.
ROUND_STRUCTURE_BASE_MAX_VALUE = 1
