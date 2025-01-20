# Version
GENERATOR_VERSION = '0.3.1'

# General generators parameters
DEFAULT_CHUNK_WIDTH = 64

# Fractal map generation
DEFAULT_DIAMOND_SQUARE_GRID_STEP = 64
DEFAULT_DIAMOND_SQUARE_GRID_MAX_VALUE = 100

# Biome generation
# DEFAULT_BIOME_GRID_STEP:  Distance between biome grid cells.
#                           Near each node will be created biome with central position +- half of grid step.
#                           Biomes area will be calculated with Voronoi algorithm.
DEFAULT_BIOME_GRID_STEP = 128
# DEFAULT_BIOME_BLEND_RADIOS:   Radios of borders smoothing between biomes.
#                               After smoothing  each point near biome borders will have average nearby biomes
#                               values with weights.
DEFAULT_BIOME_BLEND_RADIOS = 15

# Round structures generation
# DEFAULT_ROUND_STRUCTURE_GRID_STEP:    Distance between round structure grid cells.
#                                       Near each node will be created round structure with central
#                                       position +- half of grid step.
DEFAULT_ROUND_STRUCTURE_GRID_STEP = 64
# DEFAULT_ROUND_STRUCTURE_MAX_RADIUS:   Maximum distance from round structure center
#                                       which can be handled due generation.
DEFAULT_ROUND_STRUCTURE_MAX_RADIUS = 100
# DEFAULT_ROUND_STRUCTURE_MAX_VALUE:    Maximum value that can be generated with current round structure.
DEFAULT_ROUND_STRUCTURE_MAX_VALUE = 1
