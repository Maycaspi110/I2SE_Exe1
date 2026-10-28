import numpy as np
import nrrd


def load_volume(path):
    try:
        data, header = nrrd.read(str(path))
    except OSError:
        raise ValueError(str(path) + ": cannot read NRRD file") from None
    except Exception:
        raise ValueError(str(path) + ": not a valid NRRD file") from None

    if data.ndim != 3:
        raise ValueError(str(path) + ": volume must be 3-dimensional, got " + str(data.ndim))
    return data