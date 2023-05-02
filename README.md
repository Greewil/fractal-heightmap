# fractal-heightmap

## Main idea

Fractal heightmap generator allows you to create infinite self-linked maps generated randomly from seed.
It uses diamond square algorithm to create self-linked heightmaps from base point grid. 

Main advantages:
* generator can create borderless transitions in maps generated with different 
versions of this program or different seeds
* you don't need to worry about transitions between biomes
* generator can take into account already generated map chunks to increase speed
* use flexible biome generation with allows you to use your own presets of biomes
* biomes can be generated according to specified conditions

## Installation 

```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
