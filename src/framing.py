import numpy as np

"""Each image is centered within a black frame of a specific maximum size, 
ensuring that every frame in the video has the same dimensions."""

def pad_to_size(image, height, width):
    h, w = image.shape
    if h > height or w > width:
        raise ValueError("image is larger than the frame")
    frame = np.zeros((height, width), dtype=image.dtype)  # all black
    top = (height - h) // 2      # black margin above
    left = (width - w) // 2      # black margin on the left
    frame[top:top + h, left:left + w] = image
    return frame


def common_frame_size(images):
    # The frame must fit the biggest image: take the max height and max width.
    height = max(img.shape[0] for img in images)
    width = max(img.shape[1] for img in images)
    return height, width