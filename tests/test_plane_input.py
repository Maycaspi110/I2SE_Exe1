import pytest
from src.plane_input import plane_kind


def test_nine_numbers_is_triangle():
    assert plane_kind([0] * 9) == "triangle"


def test_twelve_numbers_is_trapezoid():
    assert plane_kind([0] * 12) == "trapezoid"


def test_ten_numbers_is_error():
    with pytest.raises(ValueError):
        plane_kind([0] * 10)

from src.plane_input import read_planes


def test_read_valid_file(tmp_path):
    f = tmp_path / "planes.csv"
    f.write_text("1,2,3,4,5,6,7,8,9\n\n" + ",".join(["0"] * 12) + "\n")
    planes = read_planes(f)
    assert len(planes) == 2


def test_missing_file_is_error(tmp_path):
    with pytest.raises(ValueError):
        read_planes(tmp_path / "nope.csv")


def test_non_numeric_is_error(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("1,2,abc,4,5,6,7,8,9\n")
    with pytest.raises(ValueError):
        read_planes(f)