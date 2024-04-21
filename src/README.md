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
generator = FractalGenerator(seed, chunk_width, base_grid_distance, base_grid_max_value)
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
It will generate heightmap like this:

<img src="https://github.com/Greewil/fractal-heightmap/assets/40954951/d5d81363-ffd8-4a45-b2ca-4013d1e47e75" width="256"/>

### Basic biome generation

Biomes can be used to modify generated heightmaps. 
In biome maps single tile can be part of few biomes with different weights.

Default biomes generation assumed to be based on voronoi diagram. 
In this realisation each cell of voronoi diagram will be placed close to corresponding biome grid nodes.
Neighbouring cells will be automatically blended near separation line with a little bit of noise.

To make separation lines between neighbouring cells less strait biomes generator use additional shift_map.
Its value map (like heightmap) scaled from 0 to 1 which is 1 chunk wider to the right: 
```
shift_map = Map(height_map.seed + 1, chunk_width=chunk_width)
shift_generator = FractalGenerator(shift_map.seed, chunk_width, base_grid_distance, 1)
wider_bounding = Bounding(0, 0, 1, 0)
wider_bounding.add_bounding(bounding)
wider_bounding.for_each(lambda x, y: shift_map.set_chunk(shift_generator.generate_chunk(x, y)))
```
Also, to generate biome map you need to set your own function of biome distribution. 
You can see random distribution example here: [biome usage example].

Then you can finally generate biome map:
```
biome_map = Map(seed, chunk_width=chunk_width)
biome_generator = BiomeGenerator(biome_map.seed, chunk_width, biome_grid_step, biome_blend_radios,
                                 get_random_biome_example)
bounding.for_each(lambda x, y: biome_map.set_chunk(biome_generator.generate_chunk(x, y, [shift_map])))
```
It will generate biome map like this:

<img src="https://github.com/Greewil/fractal-heightmap/assets/40954951/a2889572-8404-4584-aa16-7a57a3eff239" width="256"/>

### Using biomes to modify heightmaps

[value maps in modifiers example]

[//]: # (TODO about map modifications)


Modified heightmap will look like this:

<img src="https://github.com/Greewil/fractal-heightmap/assets/40954951/2d64c123-06ff-4bed-9059-d24b8303b42d" width="256"/>

Applied to 3D mesh modified heightmap will look like this:

<img src="https://github.com/Greewil/fractal-heightmap/assets/40954951/cc498c3b-48ad-4d48-9cd2-a78412123662" width="512"/>

### Saving maps as images

You can save height maps and biome maps as png for better result representation:
```
save_height_map_as_image(height_map, 'heightmap', max_color_value=1.5*base_grid_max_value)
save_biome_map_as_image(biome_map, 'biomes_map')
```

### More examples

You can see more code examples here: [examples]

## Contact

* Web: <https://github.com/Greewil/fractal-heightmap>
* Mail: <shishkin.sergey.d@gmail.com>

[examples]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples
[biome usage example]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples/biome_modifies_heightmap_example.py
[value maps in modifiers example]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples/biome_modifies_using_value_maps_example.py
