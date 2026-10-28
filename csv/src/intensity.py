import numpy as np

def normalize_to_uint8(values, vmin, vmax):
    """Map values from the range [vmin, vmax] to 0-255 (uint8).

    If vmin == vmax (a constant volume) the result is all zeros,
    which avoids a division by zero.
    """
    values = np.asarray(values, dtype=np.float64)
    if vmax == vmin:
        return np.zeros(values.shape, dtype=np.uint8)
    scaled = (values - vmin) / (vmax - vmin) * 255
    scaled = np.clip(scaled, 0, 255)
    return np.round(scaled).astype(np.uint8)

    