# world map generator

## Main idea

Fractal heightmap generator allows you to create infinite self-linked maps generated randomly from seed.
It uses diamond square algorithm to create self-linked heightmaps from base point grid. 

Main advantages:
* generator can create borderless transitions in maps generated with different 
versions of this program or different seeds
* you don't need to worry about transitions between biomes
* generator can take into account already generated map chunks to increase speed
* use flexible biome generation which allows you to use your own presets of biomes
* biomes can be generated according to specified conditions

## How to use

### Basic heightmap generation

To generate basic height map you can use fractal generator based on diamond square algorithm. 
Generators will return information in chunks:
```
generator = FractalGenerator(height_map.seed, chunk_width, base_grid_distance, base_grid_max_value)
height_map_chunk = generator.generate_chunk(x, y)
```
For better manipulations with chunks they could be packed in Maps:
```
height_map = Map(seed, chunk_width)
height_map.set_chunk(height_map_chunk)
```
Bounding can be used to generate rectangle of chunks:
```
bounding = Bounding(0, 0, 8, 8)
bounding.for_each(lambda x, y: height_map.set_chunk(generator.generate_chunk(x, y)))
```

### Basic biome generation

[//]: # (TODO about biome maps)

### Using biomes to modify heightmaps

[//]: # (TODO about map modifications)

### Saving maps as images

[//]: # (TODO about saving maps as images)

## Contact

* Web: <https://github.com/Greewil/fractal-heightmap>
* Mail: <shishkin.sergey.d@gmail.com>
