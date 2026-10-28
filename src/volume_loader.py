import numpy as np
import nrrd


def load_volume(path):
    # Read the 3D scan from an NRRD file and return it as a numpy array.
    try:
        data, header = nrrd.read(str(path))

        # Edge case E1: file missing or unreadable
    except OSError:
        raise ValueError(str(path) + ": cannot read NRRD file") from None

    # Edge case E2: the file is not a valid NRRD
    except Exception:
        raise ValueError(str(path) + ": not a valid NRRD file") from None

     # The volume must be a cube of 3 dimensions, not an image or video
    if data.ndim != 3:
        raise ValueError(str(path) + ": volume must be 3-dimensional, got " + str(data.ndim))
    return data