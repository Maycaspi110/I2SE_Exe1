import numpy as np
import pytest
from src.slicer import distance, unit_step


def test_distance_3_4_5():
    # Classic Pythagoras triangle: 3, 4, 5.
    # From (0,0,0) to (3,4,0) the distance must be exactly 5.
    assert distance([0, 0, 0], [3, 4, 0]) == 5.0


def test_unit_step_direction():
    # The arrow from (0,0,0) towards (3,4,0) has length 5,
    # so after dividing by 5 we expect (0.6, 0.8, 0).
    step = unit_step([0, 0, 0], [3, 4, 0])
    # allclose = "almost equal", because decimal numbers can differ
    # by a tiny amount in the computer
    assert np.allclose(step, [0.6, 0.8, 0])


def test_unit_step_has_length_one():
    # Whatever the two points are, the step must have length exactly 1.
    # We compute its length again (Pythagoras) and check it is 1.
    step = unit_step([1, 2, 3], [7, -2, 9])
    assert np.isclose(np.sqrt(np.sum(step ** 2)), 1.0)


def test_identical_points_is_error():
    # Edge case E5: two identical points have no direction.
    # We expect an error instead of a crash from dividing by zero.
    with pytest.raises(ValueError):
        unit_step([1, 1, 1], [1, 1, 1])