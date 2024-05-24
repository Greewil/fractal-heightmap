from world_map_generator.map.biome import BiomeType, are_biome_types_same, add_biome_to_biome_tile, \
    are_biome_tiles_same, biome_tile_to_dict, dict_to_biome_tile


def test_is_biome_types_same():
    biome_type_1 = BiomeType("biome 1", biome_parameters={"param 1": 1.1})
    biome_type_1_copy = BiomeType("biome 1", biome_parameters={"param 1": 1.1})
    assert are_biome_types_same(biome_type_1, biome_type_1_copy) is True
    # more params
    biome_type_2 = BiomeType("biome 1", biome_parameters={"param 1": 1.1, "param 2": 2.1})
    assert are_biome_types_same(biome_type_1, biome_type_2) is False
    # less params
    biome_type_3 = BiomeType("biome 1")
    assert are_biome_types_same(biome_type_1, biome_type_3) is False
    # different name
    biome_type_4 = BiomeType("biome 4", biome_parameters={"param 1": 1.1})
    assert are_biome_types_same(biome_type_1, biome_type_4) is False
    # different params weights
    biome_type_5 = BiomeType("biome 1", biome_parameters={"param 1": 2.1})
    assert are_biome_types_same(biome_type_1, biome_type_5) is False


def test_is_biome_tiles_same():
    biome_type_1 = BiomeType("biome 1", biome_parameters={"param 1": 1.1})
    biome_type_2 = BiomeType("biome 2", biome_parameters={"param 2": 0.5})
    biome_type_3 = BiomeType("biome 3", biome_parameters={"param 1": 0.75})
    biome_tile_1 = [(0.5, biome_type_1), (1.0, biome_type_2)]
    biome_tile_2 = [(0.5, biome_type_1), (1.0, biome_type_2)]
    assert are_biome_tiles_same(biome_tile_1, biome_tile_2) is True
    biome_tile_different_weights = [(0.5, biome_type_1), (2.0, biome_type_2)]
    assert are_biome_tiles_same(biome_tile_1, biome_tile_different_weights) is False
    biome_tile_less_types = [(0.5, biome_type_1)]
    assert are_biome_tiles_same(biome_tile_1, biome_tile_less_types) is False
    biome_tile_more_types = [(0.5, biome_type_1), (1.0, biome_type_2), (1.0, biome_type_3)]
    assert are_biome_tiles_same(biome_tile_1, biome_tile_more_types) is False
    biome_tile_different_types = [(0.5, biome_type_1), (1.0, biome_type_3)]
    assert are_biome_tiles_same(biome_tile_1, biome_tile_different_types) is False


def test_add_biome_to_biome_tile():
    biome_tile = []
    # add new
    additional_type = (1.0, BiomeType("biome 1", biome_parameters={"param 1": 1.1}))
    add_biome_to_biome_tile(biome_tile, additional_type)
    current_biome_tile = [(1.0, BiomeType("biome 1", biome_parameters={"param 1": 1.1}))]
    assert are_biome_tiles_same(biome_tile, current_biome_tile)
    # add same
    additional_type = (2.5, BiomeType("biome 1", biome_parameters={"param 1": 1.1}))
    add_biome_to_biome_tile(biome_tile, additional_type)
    current_biome_tile = [(3.5, BiomeType("biome 1", biome_parameters={"param 1": 1.1}))]
    assert are_biome_tiles_same(biome_tile, current_biome_tile)
    # add new (different name)
    additional_type = (0.5, BiomeType("biome 2", biome_parameters={"param 1": 1.1}))
    add_biome_to_biome_tile(biome_tile, additional_type)
    current_biome_tile = [(3.5, BiomeType("biome 1", biome_parameters={"param 1": 1.1})),
                          (0.5, BiomeType("biome 2", biome_parameters={"param 1": 1.1}))]
    assert are_biome_tiles_same(biome_tile, current_biome_tile)
    # add new (different param)
    additional_type = (0.5, BiomeType("biome 2", biome_parameters={"param 1": 0.1}))
    add_biome_to_biome_tile(biome_tile, additional_type)
    current_biome_tile = [(3.5, BiomeType("biome 1", biome_parameters={"param 1": 1.1})),
                          (0.5, BiomeType("biome 2", biome_parameters={"param 1": 1.1})),
                          (0.5, BiomeType("biome 2", biome_parameters={"param 1": 0.1}))]
    assert are_biome_tiles_same(biome_tile, current_biome_tile)
    # add same
    additional_type = (0.5, BiomeType("biome 2", biome_parameters={"param 1": 0.1}))
    add_biome_to_biome_tile(biome_tile, additional_type)
    current_biome_tile = [(3.5, BiomeType("biome 1", biome_parameters={"param 1": 1.1})),
                          (0.5, BiomeType("biome 2", biome_parameters={"param 1": 1.1})),
                          (1.0, BiomeType("biome 2", biome_parameters={"param 1": 0.1}))]
    assert are_biome_tiles_same(biome_tile, current_biome_tile)


def test_convert_biome_tile_to_dict():
    biome_type_1 = BiomeType("biome 1", biome_parameters={"param 1": 1.1})
    biome_type_2 = BiomeType("biome 2", biome_parameters={"param 2": 0.5})
    biome_type_3 = BiomeType("biome 3", biome_parameters={"param 1": 0.75})
    biome_tile_1 = [(0.5, biome_type_1), (1.0, biome_type_2), (-0.75, biome_type_3)]
    biome_tile_1_as_dict = biome_tile_to_dict(biome_tile_1)
    assert len(biome_tile_1_as_dict.keys()) == 3
    assert biome_tile_1_as_dict.get("biome 1").get("weight") == 0.5
    assert biome_tile_1_as_dict.get("biome 1").get("params") == {"param 1": 1.1}
    assert biome_tile_1_as_dict.get("biome 2").get("weight") == 1.0
    assert biome_tile_1_as_dict.get("biome 2").get("params") == {"param 2": 0.5}
    assert biome_tile_1_as_dict.get("biome 3").get("weight") == -0.75
    assert biome_tile_1_as_dict.get("biome 3").get("params") == {"param 1": 0.75}

    biome_tile_2 = []
    biome_tile_2_as_dict = biome_tile_to_dict(biome_tile_2)
    assert len(biome_tile_2_as_dict.keys()) == 0


def test_convert_dict_to_biome_tile():
    biome_type_1 = BiomeType("biome 1")
    biome_type_2 = BiomeType("biome 2")
    biomes_list = [biome_type_1, biome_type_2]
    biome_tile_dict = {
        "biome 1": {
            "weight": 0.5,
            "params": {"param 1": 1.1}
        },
        "biome 2": {
            "weight": 1.0,
            "params": {
                "param 2": 0.5,
                "param 3": 0.75
            }
        }
    }
    biome_tile = dict_to_biome_tile(biome_tile_dict, biomes_list)
    converted_back = biome_tile_to_dict(biome_tile)
    assert biome_tile_dict == converted_back
