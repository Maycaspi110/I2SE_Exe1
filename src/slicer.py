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