import numpy as np
import pytest
from src.framing import pad_to_size, common_frame_size


#A small image (a 2×2 grid containing 7s) is placed in the center of a 4×4 black frame, resulting in 7s in the middle and black areas in the corners. 
# An image larger than the frame cannot fit; therefore, an error should be thrown instead of the program crashing. 
# The dimensions of the combined frame are determined by the maximum height and maximum width among all the images.
def test_pad_centers_image():
    # A 2x2 image of 7s inside a 4x4 black frame sits in the middle
    image = np.full((2, 2), 7, dtype=np.uint8)
    frame = pad_to_size(image, 4, 4)
    assert frame.shape == (4, 4)
    assert frame[1, 1] == 7      # inside the image
    assert frame[0, 0] == 0      # black margin


def test_image_too_big_is_error():
    image = np.ones((5, 5), dtype=np.uint8)
    with pytest.raises(ValueError):
        pad_to_size(image, 4, 4)

#A 3×8 image and a 6×2 image: the maximum height is 6 and the maximum width is 8, so the frame is 6×8. 
# It cannot be 6×2, because the first image (with a width of 8) would not fit. The frame must accommodate all of them.
def test_common_size_is_the_maximum():
    a = np.zeros((3, 8))
    b = np.zeros((6, 2))
    assert common_frame_size([a, b]) == (6, 8)