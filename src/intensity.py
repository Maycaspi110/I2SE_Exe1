import numpy as np


def normalize_to_uint8(values, vmin, vmax):
    values = np.asarray(values, dtype=np.float64)
    if vmax == vmin:
        return np.zeros(values.shape, dtype=np.uint8)
    scaled = (values - vmin) / (vmax - vmin) * 255
    scaled = np.clip(scaled, 0, 255)
    return np.round(scaled).astype(np.uint8)