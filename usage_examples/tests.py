from world_map_generator.map import Map
from world_map_generator.map.chunk import ValueChunk, BiomeChunk

if __name__ == '__main__':
    # TODO make real tests

    # should raise exception
    # chunk1 = ValueChunk(1, 14, 64)
    # chunk2 = ValueChunk(1, 14, 128, chunk1.tiles)

    # should be ok
    chunk1 = ValueChunk(1, 14, 64)
    chunk2 = ValueChunk(1, 14, chunk1.chunk_width, chunk1.tiles)

    # should raise exception
    test_map = Map()
    chunk_v = ValueChunk(1, 1)
    test_map.set_chunk(chunk_v)
    chunk_b = BiomeChunk(1, 2)
    test_map.set_chunk(chunk_b)

    # should be ok
    # test_map = Map()
    # chunk_1 = ValueChunk(1, 1)
    # test_map.set_chunk(chunk_1)
    # chunk_2 = ValueChunk(1, 2)
    # test_map.set_chunk(chunk_2)
