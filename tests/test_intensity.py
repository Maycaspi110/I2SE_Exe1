from src.intensity import normalize_to_uint8


def test_quarter_value():
    # 250 in range 0-1000 is a quarter of the way about 64
    assert normalize_to_uint8(250, 0, 1000) == 64


def test_above_max_is_white():
    # 1500 is above the max, so it is clipped to 255
    assert normalize_to_uint8(1500, 0, 1000) == 255


def test_below_min_is_black():
    # -200 is below the min, so it is clipped to 0
    assert normalize_to_uint8(-200, 0, 1000) == 0


def test_constant_volume_gives_zero():
    # min == max: no division by zero, result is black
    assert normalize_to_uint8(7, 7, 7) == 0