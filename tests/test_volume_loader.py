import numpy as np
import nrrd
import pytest
from src.volume_loader import load_volume


def test_load_valid_volume(tmp_path):
    f = tmp_path / "v.nrrd"
    nrrd.write(str(f), np.zeros((4, 5, 6), dtype=np.uint8))
    data = load_volume(f)
    assert data.shape == (4, 5, 6)


def test_missing_file_is_error(tmp_path):
    with pytest.raises(ValueError):
        load_volume(tmp_path / "nope.nrrd")


def test_2d_volume_is_error(tmp_path):
    f = tmp_path / "flat.nrrd"
    nrrd.write(str(f), np.zeros((4, 5), dtype=np.uint8))
    with pytest.raises(ValueError):
        load_volume(f)