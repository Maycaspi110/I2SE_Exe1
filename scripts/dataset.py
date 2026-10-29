import os
import numpy as np
import nrrd


def make_log(size=100):
    # A "tree trunk": the value depends on the distance from the central axis.
    # Cutting across it gives concentric circles, cutting along it gives stripes.
    x, y, z = np.indices((size, size, size))
    center = (size - 1) / 2
    distance = np.sqrt((x - center) ** 2 + (y - center) ** 2)
    rings = (np.sin(distance / 3) + 1) / 2 * 200 + 20
    rings[distance > size / 2 - 1] = 0
    return rings.astype(np.uint8)


if __name__ == "__main__":
    os.makedirs("data-NRRD", exist_ok=True)
    nrrd.write("data-NRRD/tree_trunk.nrrd", make_log())
    print("created data-NRRD/tree_trunk.nrrd")