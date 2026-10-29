import cv2
import numpy as np
from src.video_writer import write_video

"""The test includes three images of different sizes: (4,6), (8,5), and (3,3).
We define a video file path in a temporary directory, `tmp_path`.
We then open the video file using `cv2.VideoCapture` and retrieve its properties.
Verification:
3 frames—one frame for each image. The common dimensions are determined by the maximum width 6 and the maximum height 8."""
def test_video_has_one_frame_per_image(tmp_path):
    images = [np.ones((4, 6)), np.ones((8, 5)), np.ones((3, 3))]
    out = tmp_path / "out.mp4"
    write_video(images, 0, 1, out)
    video = cv2.VideoCapture(str(out))
    assert int(video.get(cv2.CAP_PROP_FRAME_COUNT)) == 3
    # every frame has the common size: width 6, height 8
    assert int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) == 6
    assert int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) == 8
    video.release()