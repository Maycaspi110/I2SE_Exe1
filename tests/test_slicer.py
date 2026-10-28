import numpy as np
import pytest
from src.slicer import distance, unit_step


def test_distance_3_4_5():
    # Classic Pythagoras triangle: 3, 4, 5.
    # From (0,0,0) to (3,4,0) the distance must be exactly 5.
    assert distance([0, 0, 0], [3, 4, 0]) == 5.0



 # The arrow from (0,0,0) towards (3,4,0) has length 5,
    # so after dividing by 5 we expect (0.6, 0.8, 0).
def test_unit_step_direction():
    step = unit_step([0, 0, 0], [3, 4, 0])
    # allclose = "almost equal", because decimal numbers can differ
    # by a tiny amount in the computer
    assert np.allclose(step, [0.6, 0.8, 0])


 # Whatever the two points are, the step must have length exactly 1.
    # We compute its length again (Pythagoras) and check it is 1.
def test_unit_step_has_length_one():
    step = unit_step([1, 2, 3], [7, -2, 9])
    assert np.isclose(np.sqrt(np.sum(step ** 2)), 1.0)


def test_identical_points_is_error():
    # Edge case E5: two identical points have no direction.
    # We expect an error instead of a crash from dividing by zero.
    with pytest.raises(ValueError):
        unit_step([1, 1, 1], [1, 1, 1])


from src.slicer import sample_voxel


def test_sample_inside_returns_value():
    # A 2x2x2 cube where each cell holds its own number 0..7
    volume = np.arange(8).reshape(2, 2, 2)
    # Point (1,1,1) is the last cell, value 7
    assert sample_voxel(volume, [1, 1, 1]) == 7


def test_sample_rounds_to_nearest():
    volume = np.arange(8).reshape(2, 2, 2)
    # 0.9 rounds to 1, so this is the same cell as (1,1,1)
    assert sample_voxel(volume, [0.9, 0.9, 0.9]) == 7


def test_sample_outside_returns_zero():
    volume = np.ones((2, 2, 2))
    # Outside the cube in every direction: black
    assert sample_voxel(volume, [5, 5, 5]) == 0
    assert sample_voxel(volume, [-1, 0, 0]) == 0