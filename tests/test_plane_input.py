import pytest
from src.plane_input import plane_kind


def test_nine_numbers_is_triangle():
    assert plane_kind([0] * 9) == "triangle"


def test_twelve_numbers_is_trapezoid():
    assert plane_kind([0] * 12) == "trapezoid"


def test_ten_numbers_is_error():
    with pytest.raises(ValueError):
        plane_kind([0] * 10)