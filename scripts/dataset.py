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


def make_slicer_log(size=100):
    # A 16-bit "tree trunk" for 3D Slicer. Same idea as make_log (rings around
    # the central axis), with growth rings of changing width, a soft center, a
    # bright bark layer and a slightly bending axis. The trunk gets thinner towards
    # the top and has two branches, so every layer (z) looks different when you
    # scroll through the slices.
    x, y, z = np.indices((size, size, size))
    center = (size - 1) / 2
    cx = center + 3 * np.sin(z / 22)             # the axis bends a little along z
    cy = center + 2 * np.cos(z / 30)
    distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    phase = distance * 0.38 + 0.3 * np.sin(distance * 0.1)   # ring width changes slowly
    wood = 1200 + 1300 * (np.sin(phase) + 1) / 2
    radius = (size / 2 - 1) * (1 - 0.25 * z / (size - 1))    # thinner towards the top
    wood[distance < 3] = 800                      # soft center (pith)
    wood[distance > radius - 4] = 3400            # bright bark layer
    wood[distance > radius] = 0                   # air around the trunk
    # two branches, they leave the trunk at different heights and directions
    branch1 = ((y - cy) ** 2 + (z - 32) ** 2 < 5 ** 2) & (x > cx)
    branch2 = ((x - cx) ** 2 + (z - 66) ** 2 < 4 ** 2) & (y < cy)
    wood[(branch1 | branch2) & (distance > 3)] = 2400
    return wood.astype(np.uint16)


def write_for_slicer(path, volume, voxel_mm=1.0):
    # Header fields that 3D Slicer reads: orientation, voxel size in mm and origin.
    # Without them Slicer still opens the file, but guesses the geometry.
    header = {
        "space": "left-posterior-superior",
        "space directions": np.diag([voxel_mm] * 3),
        "space origin": -(np.array(volume.shape) - 1) / 2 * voxel_mm,   # volume centered at 0
        "kinds": ["domain", "domain", "domain"],
        "encoding": "gzip",
    }
    nrrd.write(path, volume, header)


if __name__ == "__main__":
    os.makedirs("data-NRRD", exist_ok=True)
    nrrd.write("data-NRRD/tree_trunk.nrrd", make_log())
    print("created data-NRRD/tree_trunk.nrrd")
    write_for_slicer("data-NRRD/tree_trunk_slicer.nrrd", make_slicer_log())
    print("created data-NRRD/tree_trunk_slicer.nrrd")