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

#Constructing a 2D image of the plane using two runners, a1 and a2.
def project_plane(volume, start1, start2, b, c):
    #a1 and a2 from start 1 and start 2 run to b and c 
    start1 = np.asarray(start1, dtype=np.float64)
    start2 = np.asarray(start2, dtype=np.float64)

    height = int(np.ceil(distance(start1, b)))   # number of rows (Dab)
    width = int(np.ceil(distance(b, c)))         # widest row (Dbc)
    image = np.zeros((height, width + 1), dtype=volume.dtype)  # all black

    step1 = unit_step(start1, b)   
    step2 = unit_step(start2, c)  
    a1, a2 = start1, start2

    for y in range(height):
        a1 = a1 + step1
        a2 = a2 + step2
        row = build_row(volume, a1, a2)
        
        # Center the row inside the image width
        x_start = int(round((width - len(row)) / 2))
        for i, value in enumerate(row):
            x = x_start + i
            if 0 <= x < image.shape[1]:    # ignore writes outside the image
                image[y, x] = value
    return image