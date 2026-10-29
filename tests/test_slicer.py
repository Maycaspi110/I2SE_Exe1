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


from src.slicer import build_row


 # Cube where the value equals x: cell x=0 holds 0, or 1, or 2..
def test_build_row_reads_along_a_line():
    volume = np.zeros((4, 1, 1))
    for x in range(4):
        volume[x, 0, 0] = x
    # Walk from x=0 to x=3 along the x axis: expect 0,1,2,3
    assert build_row(volume, [0, 0, 0], [3, 0, 0]) == [0, 1, 2, 3]


def test_build_row_same_point_is_one_pixel():
    volume = np.full((2, 2, 2), 9)
    assert build_row(volume, [1, 1, 1], [1, 1, 1]) == [9]


from src.slicer import project_plane


"""
We have a function that takes a cube and a triangle as input and returns an image.

Test 1":
Construct a cube—a 20×20×20 cube works well—where every cell contains the number 5; essentially a uniform block consisting entirely of "5"s. Place a triangle inside it. 
If the result is 5, we know that the point lies inside."""
def test_project_plane_constant_volume():
    volume = np.full((20, 20, 20), 5, dtype=np.uint8)
    # Triangle in the z=10 layer, apex (10,0,10), base (5..15, 10, 10)
    image = project_plane(volume, [10, 0, 10], [10, 0, 10],
                          [5, 10, 10], [15, 10, 10])
    assert image.ndim == 2
    assert image.max() == 5      # plane pixels read the cube
    assert image[0, 0] == 0      # corner outside the triangle stays black
    

""" Test 2: Anything that does not return the value 9 is not contained within 
therefore, everything is 0—that is, black."""

def test_project_plane_outside_is_black():
    volume = np.full((5, 5, 5), 9, dtype=np.uint8)
    # Plane far away from the cube: the whole image is black
    image = project_plane(volume, [100, 100, 100], [100, 100, 100],
                          [105, 110, 100], [95, 110, 100])
    assert image.max() == 0