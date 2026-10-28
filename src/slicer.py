import numpy as np


def distance(p, q):
    # Straight-line distance between two 3D points p and q.
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    return float(np.sqrt(np.sum((q - p) ** 2)))


def unit_step(p, q):
    # An arrow of length exactly 1 pointing from p towards q.
    # Adding it to a point moves us one unit in that direction.
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    d = distance(p, q)
    if d == 0:
        raise ValueError("cannot compute a direction between identical points")
    return (q - p) / d

# Return the value of the volume at a 3D point.
    # The point is rounded to the nearest voxel (our design decision).
    # A point outside the volume gives 0 (black), as the assignment says.
def sample_voxel(volume, point):
    x, y, z = np.round(point).astype(int)
    sx, sy, sz = volume.shape
    if 0 <= x < sx and 0 <= y < sy and 0 <= z < sz:
        return volume[x, y, z]
    return 0


 # Build one row of the image: walk from point a1 to point a2
    # in steps of length 1, and read the cube value at every step.
def build_row(volume, a1, a2):
    a1 = np.asarray(a1, dtype=np.float64)
    a2 = np.asarray(a2, dtype=np.float64)

    d12 = distance(a1, a2)           # how long the row is
    if d12 == 0:
        return [sample_voxel(volume, a1)]   # both points are the same: one pixel

    step = unit_step(a1, a2)         # one step of length 1 towards a2
    row = []
    p = a1
    for _ in range(int(d12) + 1):    # one pixel per step, including both ends
        row.append(sample_voxel(volume, p))
        p = p + step                 # move one step forward
    return row