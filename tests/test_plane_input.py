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

# valid planes used by the tests below
TRIANGLE = "5,0,0,0,10,0,10,10,0"                 # |ab| = |ac|
TRAPEZOID = "4,0,0,0,10,0,6,0,0,10,10,0"          # a', b, a'', c: both legs are equal


def test_read_valid_file(tmp_path):
    f = tmp_path / "planes.csv"
    f.write_text(TRIANGLE + "\n\n" + TRAPEZOID + "\n")
    planes = read_planes(f)
    assert len(planes) == 2


def test_missing_file_is_error(tmp_path):
    with pytest.raises(ValueError):
        read_planes(tmp_path / "nope.csv")


def test_non_numeric_is_error(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("5,0,abc,0,10,0,10,10,0\n")
    with pytest.raises(ValueError):
        read_planes(f)


def test_header_and_point_count_column(tmp_path):
    # Layout with a header line and the number of points as first column
    f = tmp_path / "header.csv"
    f.write_text("Number of Points (3 or 4),x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4\n"
                 "3," + TRIANGLE + ",,,\n"
                 "4," + TRAPEZOID + "\n")
    planes = read_planes(f)
    assert [len(p) for p in planes] == [9, 12]


def test_triangle_not_isosceles_is_error(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text(TRIANGLE + "\n1,2,3,4,5,6,7,8,9\n")
    with pytest.raises(ValueError, match="row 2"):
        read_planes(f)


def test_trapezoid_legs_different_is_error(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("4,0,0,0,10,0,6,0,0,12,10,0\n")
    with pytest.raises(ValueError, match="row 1"):
        read_planes(f)


def test_trapezoid_not_on_one_plane_is_error(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("4,0,0,0,10,0,6,0,0,10,10,5\n")
    with pytest.raises(ValueError, match="row 1"):
        read_planes(f)
