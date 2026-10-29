# Creates the illustration images in images/: cross-sections of the tree trunk
# volumes, computed with the project's own projection (src/slicer.py).
# Usage (from the project folder): python scripts/make_figures.py
import os
import sys
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.volume_loader import load_volume
from src.slicer import project_plane_fast
from src.intensity import normalize_to_uint8

SCALE = 3                      # a voxel is drawn as 3x3 pixels (illustration only), smaller if it does not fit
PANEL = 330                    # size of one panel in pixels
FONT = cv2.FONT_HERSHEY_SIMPLEX
VOLUMES = [("tree_trunk", "Tree trunk, 8-bit", 1.0),
           ("tree_trunk_slicer", "Tree trunk for 3D Slicer, 16-bit", 1.0)]


def plane_points(center, u, v, half_width, half_height):
    # the 4 points a', b, a'', c of a rectangle: u runs along a row, v down the image
    top, bottom = center - half_height * v, center + half_height * v
    return top - half_width * u, bottom - half_width * u, top + half_width * u, bottom + half_width * u


def views(shape):
    center = (np.array(shape) - 1) / 2
    x, y, z = np.eye(3)
    tilt = np.radians(40)
    oblique = np.array([0, np.cos(tilt), np.sin(tilt)])
    return [("Cross-section (z = middle)", plane_points(center, x, y, 50, 50)),
            ("Lengthwise (y = middle)", plane_points(center, x, z, 50, 50)),
            ("Oblique (40 degrees tilt)", plane_points(center, x, oblique, 50, 60))]


def text(img, string, x, y, size=0.5, color=(255, 255, 255)):
    cv2.putText(img, string, (x, y), FONT, size, color, 1, cv2.LINE_AA)


def panel(volume, vmin, vmax, voxel_mm, title, points):
    a1, b, a2, c = points
    image = project_plane_fast(volume, a1, a2, b, c)
    gray = normalize_to_uint8(image, vmin, vmax)
    scale = min(SCALE, (PANEL - 8) / max(gray.shape))
    big = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
    canvas = np.zeros((PANEL + 60, PANEL, 3), dtype=np.uint8)
    h, w = big.shape
    top, left = 28 + (PANEL - h) // 2, (PANEL - w) // 2
    canvas[top:top + h, left:left + w] = big[:, :, None]
    text(canvas, title, 8, 18)
    bar = int(round(20 / voxel_mm * scale))             # scale bar of 2 cm
    cv2.line(canvas, (8, PANEL + 40), (8 + bar, PANEL + 40), (255, 255, 255), 2)
    text(canvas, "2 cm", 8 + bar + 8, PANEL + 45, 0.4)
    return canvas


def figure(name, caption, voxel_mm):
    volume = load_volume(f"data-NRRD/{name}.nrrd")
    vmin, vmax = volume.min(), volume.max()
    sx, sy, sz = volume.shape
    info = f"{name}.nrrd   {sx} x {sy} x {sz} voxels of {volume.dtype}, voxel {voxel_mm:g} x {voxel_mm:g} x {voxel_mm:g} mm"
    panels = [panel(volume, vmin, vmax, voxel_mm, t, p) for t, p in views(volume.shape)]
    header = np.zeros((34, PANEL * len(panels), 3), dtype=np.uint8)
    text(header, caption + "   |   " + info, 8, 22, 0.5)
    return np.vstack([header, np.hstack(panels)])


def layers(name, caption, voxel_mm, heights=(10, 32, 50, 66, 90)):
    # cross-sections at different heights z: what you see when you scroll through the layers
    volume = load_volume(f"data-NRRD/{name}.nrrd")
    vmin, vmax = volume.min(), volume.max()
    x, y, z = np.eye(3)
    panels = []
    for height in heights:
        center = (np.array(volume.shape) - 1) / 2
        center[2] = height
        panels.append(panel(volume, vmin, vmax, voxel_mm, f"Cross-section z = {height}", plane_points(center, x, y, 50, 50)))
    header = np.zeros((34, PANEL * len(panels), 3), dtype=np.uint8)
    text(header, caption, 8, 22, 0.5)
    return np.vstack([header, np.hstack(panels)])



def filmstrip(video_path, caption, count=6, size=165):
    # `count` frames, evenly spaced, taken from a result video
    video = cv2.VideoCapture(video_path)
    total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    row = []
    for index in np.linspace(0, total - 1, count).astype(int):
        video.set(cv2.CAP_PROP_POS_FRAMES, int(index))
        ok, frame = video.read()
        scale = (size - 4) / max(frame.shape[:2])
        small = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        tile = np.zeros((size + 24, size, 3), dtype=np.uint8)
        top, left = (size - small.shape[0]) // 2, (size - small.shape[1]) // 2
        tile[top:top + small.shape[0], left:left + small.shape[1]] = small
        text(tile, f"frame {index + 1}/{total}", 8, size + 16, 0.4)
        row.append(tile)
    video.release()
    header = np.zeros((28, size * count, 3), dtype=np.uint8)
    text(header, caption, 8, 19)
    return np.vstack([header, np.hstack(row)])


if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)
    figures = []
    for name, caption, voxel in VOLUMES:
        img = figure(name, caption, voxel)
        cv2.imwrite(f"images/{name}.png", img)
        figures.append(img)
        print(f"created images/{name}.png")
    cv2.imwrite("images/overview.png", np.vstack(figures))
    print("created images/overview.png")
    cv2.imwrite("images/layers.png", layers("tree_trunk_slicer", "Layers of the 16-bit trunk: the cross-section changes with the height (thinner trunk, two branches)", 1.0))
    print("created images/layers.png")
    strip = filmstrip("video/tree_trunk_slicer_tilt.mp4",
                      "Video of trunk_tilt.csv: the plane tilts from a cross-section to a lengthwise cut")
    cv2.imwrite("images/video_frames.png", strip)
    print("created images/video_frames.png")
