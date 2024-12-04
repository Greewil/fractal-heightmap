# world-map-generator
[![release](https://badgen.net/github/release/Greewil/fractal-heightmap/stable)](https://github.com/Greewil/fractal-heightmap/releases)
[![Last updated](https://img.shields.io/github/release-date/Greewil/fractal-heightmap?label=updated)](https://github.com/Greewil/fractal-heightmap/releases)

Actions with repository: [create fork](https://github.com/Greewil/fractal-heightmap/fork), [watch repo](https://github.com/Greewil/fractal-heightmap/subscription), [create issue](https://github.com/Greewil/fractal-heightmap/issues/new)

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

To generate basic heightmap you can use fractal generator based on diamond square algorithm. 
Generators will return information in chunks:
```
generator = FractalGenerator(seed, chunk_width, base_grid_distance, base_grid_max_value)
height_map_chunk = generator.generate_chunk(x, y)
```
Chunks could be packed in Maps for better manipulations with them:
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
A single tile can belong to multiple biomes with corresponding weights.

Default biomes generation is based on voronoi diagram. 
In this realisation each cell of voronoi diagram will be placed close to corresponding biome grid nodes.
Neighbouring cells will be automatically blended near separation line with a little bit of noise (dithering).

To make separation lines between neighbouring cells not as sharp biomes generator use additional shift_map.
Shift map is analog of heightmap but scaled from 0 to 1. 
Also shift map is 1 chunk wider to the right to use it as shift map for both axes.
So shift map could be generated like this: 
```
shift_map = Map(height_map.seed + 1, chunk_width=chunk_width)
shift_generator = FractalGenerator(shift_map.seed, chunk_width, base_grid_distance, 1)
wider_bounding = Bounding(0, 0, 1, 0)
wider_bounding.add_bounding(bounding)
wider_bounding.for_each(lambda x, y: shift_map.set_chunk(shift_generator.generate_chunk(x, y)))
```

Ofcourse you need to set up biome types before generating biome map. 
Mainly biome parameters will affect function of biome distribution and heightmap modification process later.
```
biome_example_1 = BiomeType(title='biome 1',
                            biome_parameters={'appearance_weight': 2},
                            height_modification=your_modifier_1)
biome_example_2 = BiomeType(title='biome 2',
                            biome_parameters={'appearance_weight': 0.5},
                            height_modification=your_modifier_2)
```

Also, you need to set your own function of biome distribution. 
For example random biome distribution according to weights:
```
biome_types_pool = [biome_example_1, biome_example_2]
biomes_weights = [b.biome_parameters['appearance_weight'] for b in biome_types_pool]
biomes_cumulative_distribution = get_cumulative_distribution_list(biomes_weights)


def get_random_biome_example(biome_node_x: int, biome_node_y: int, seed: int) -> BiomeType:
    pos_seed = get_position_seed(biome_node_x, biome_node_y, seed + 69)
    biome_index = weighted_random_selection(biomes_cumulative_distribution, pos_seed)
    return biome_types_pool[biome_index]
```

Then you can finally generate biome map using your own get_biome_type method to set biome distribution:
```
biome_map = Map(seed, chunk_width=chunk_width)
biome_generator = BiomeGenerator(biome_map.seed, chunk_width, biome_grid_step, biome_blend_radios,
                                 get_biome_type)
bounding.for_each(lambda x, y: biome_map.set_chunk(biome_generator.generate_chunk(x, y, [shift_map])))
```
It will generate biome map like this:

<img src="https://github.com/Greewil/fractal-heightmap/assets/40954951/a2889572-8404-4584-aa16-7a57a3eff239" width="256"/>

### Using biomes to modify heightmaps

When you have biome map you can modify any heightmap with height_modification function set in each biome.
```
modifier = MapModifier(biome_map.seed, chunk_width)
bounding.for_each(modify_heightmap_chunk)
bounding.for_each(lambda x, y: height_map.set_chunk(modifier.modify_heightmap_chunk(x, y,
                                                    height_map.get_chunk(x, y),
                                                    biome_map.get_chunk(x, y))))
```
If there are few biomes at handling tile so the resulting value will be the summ of weighted results for all biomes.

Modified heightmap will look like this:

<img src="https://github.com/Greewil/fractal-heightmap/assets/40954951/2d64c123-06ff-4bed-9059-d24b8303b42d" width="256"/>

Applied to 3D mesh modified heightmap will look like this:

<img src="https://github.com/Greewil/fractal-heightmap/assets/40954951/cc498c3b-48ad-4d48-9cd2-a78412123662" width="512"/>

For more details, see this example: [biome usage example].

Your modification methods can use another maps like in this example: [value maps in modifiers example].

### Saving maps as images

You can save height maps and biome maps as png for better result representation:
```
save_height_map_as_image(height_map, 'heightmap', max_color_value=1.5*base_grid_max_value)
save_biome_map_as_image(biome_map, 'biomes_map')
```

### Map composing

You can use MapComposer to combine few maps into one new:
[map composing example].

### Map distortion

You can distort maps with DistortionGenerator using any shift map you want: 
[distortion maps example].

### Round structures maps

You can generate round structures with DotsGenerator: 
[round structures example].

### More examples

One of the common noise realizations is ridged noise. 
It's realization with distortion will look like this:

<img src="https://github.com/Greewil/fractal-heightmap/assets/40954951/fdbc53d0-8175-4375-8422-168c3e540519" width="256"/>

See realization here: [ridged noise example].

You can see more code examples here: [examples].

## Installation

```
pip install world-map-generator
```

For more info you can visit [pypi page](https://pypi.org/project/world-map-generator/).

## License

fractal-heightmap is licensed under the terms of the MIT License. See [LICENSE] file.

## Contact

* Web: <https://github.com/Greewil/fractal-heightmap>
* Mail: <shishkin.sergey.d@gmail.com>

[LICENSE]: https://github.com/Greewil/fractal-heightmap/blob/main/LICENSE
[examples]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples
[biome usage example]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples/biome_modifies_heightmap_example.py
[value maps in modifiers example]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples/biome_modifies_using_value_maps_example.py
[round structures example]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples/round_structures_map_examples.py
[distortion maps example]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples/map_distortion_examples.py
[map composing example]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples/map_composing_examples.py
[ridged noise example]: https://github.com/Greewil/fractal-heightmap/blob/main/usage_examples/ridged_noise_examples.py
