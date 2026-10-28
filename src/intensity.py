import numpy as np

# Convert scan values gray levels 0-255 for the video.
# vmin/vmax are the min and max of the WHOLE volume, computed once so the same value always gets the same brightness in every frame.

def normalize_to_uint8(values, vmin, vmax):
    values = np.asarray(values, dtype=np.float64) 

    # Edge case E7: all voxels equal -> division by zero, return blac
    if vmax == vmin:
        return np.zeros(values.shape, dtype=np.uint8)
    scaled = (values - vmin) / (vmax - vmin) * 255
    scaled = np.clip(scaled, 0, 255) # anything outside the range is cut to 0/255
    return np.round(scaled).astype(np.uint8) # round, then whole numbers 0-255