import pytest
from world_map_generator.utils import Bounding


@pytest.mark.parametrize("borders, elements_total, elements_total_exclude_border", [
    ((0, 0, 1, 1), 4, 1), ((0, 0, 3, 2), 12, 6), ((0, 0, 0, 9), 10, 0),
])
def test_for_each(borders, elements_total, elements_total_exclude_border):
    bounding = Bounding(borders[0], borders[1], borders[2], borders[3])
    elements_handled = set()
    bounding.for_each(lambda x, y: elements_handled.add((x, y)))
    assert len(elements_handled) == elements_total

    elements_handled_exclude_border = set()
    bounding.for_each(lambda x, y: elements_handled_exclude_border.add((x, y)), False)
    assert len(elements_handled_exclude_border) == elements_total_exclude_border


@pytest.mark.parametrize("bounding, additional_bounding, final_bounding", [
    (Bounding(0, 0, 1, 1), Bounding(0, 1, 4, -2),
     Bounding(0, 1, 5, -1)),
    (Bounding(-1_000_000_000_000, 1_000_000_000_000, 0, 0), Bounding(0, 0, 1_000_000_000_000, -1_000_000_000_000),
     Bounding(-1_000_000_000_000, 1_000_000_000_000, 1_000_000_000_000, -1_000_000_000_000)),
])
def test_add_bounding(bounding, additional_bounding, final_bounding):
    bounding.add_bounding(additional_bounding)
    assert bounding == final_bounding


@pytest.mark.parametrize("bounding, additional_size, final_bounding", [
    (Bounding(0, 0, 1, 1), 4, Bounding(-4, -4, 5, 5)),
    (Bounding(-1, -1, 1, 2), 1_000_000_000_000,
     Bounding(-1_000_000_000_001, -1_000_000_000_001, 1_000_000_000_001, 1_000_000_000_002)),
])
def test_get_wider_bounding(bounding, additional_size, final_bounding):
    wider_bounding = bounding.get_wider_bounding(additional_size)
    assert wider_bounding == final_bounding


@pytest.mark.parametrize("bounding, point_x, point_y, final_bounding", [
    (Bounding(0, 0, 1, 1), 4, 5, Bounding(0, 0, 4, 5)),
    (Bounding(1, 1, 1, 1), -1_000_000_000_000, 1_000_000_000_000,
     Bounding(-1_000_000_000_000, 1, 1, 1_000_000_000_000)),
])
def test_update_min_max(bounding, point_x, point_y, final_bounding):
    bounding.update_min_max(point_x, point_y)
    assert bounding == final_bounding
