import cv2
import numpy as np
from src.framing import pad_to_size, common_frame_size
from src.intensity import normalize_to_uint8

""" Converting a list of 2D images for each plane into an MP4 video.
 vmin/vmax: The minimum and maximum values ​​for the entire volume, to ensure consistent brightness."""

def write_video(images, vmin, vmax, path, fps=30):
    if len(images) == 0:
        raise ValueError("no images to write")

    # All frames must have the same size: the biggest image decides
    height, width = common_frame_size(images)

    # OpenCV wants width, height here, the opposite order of numpy
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"),
                             fps, (width, height), isColor=False)
    if not writer.isOpened():
        raise ValueError(str(path) + ": cannot create video file")

    for image in images:
        frame = pad_to_size(image, height, width) # same size for all
        frame = normalize_to_uint8(frame, vmin, vmax) # gray levels 0-255
        writer.write(frame)   # add the frame
    writer.release() 