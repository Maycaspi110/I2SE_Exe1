# Creates the CSV files with the planes for the 100x100x100 tree trunk volumes
# (data-NRRD/tree_trunk.nrrd and data-NRRD/tree_trunk_slicer.nrrd).
#   trunk_sweep.csv  : 90 triangles, the plane moves along the z axis (cross-sections)
#   trunk_rotate.csv : 120 trapezoids, a lengthwise plane turns around the trunk axis
#   trunk_tilt.csv   : 120 trapezoids, a plane through the center tilts from a
#                      cross-section to a lengthwise cut and back
import os
import numpy as np

HEADER = "Number of Points (3 or 4),x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4"
CENTER = np.array([49.5, 49.5, 49.5])      # center of a 100x100x100 volume


def row(points):
    numbers = ",".join(f"{v:.6f}" for p in points for v in p)
    return f"{len(points)},{numbers}"


def trapezoid(center, u, v, half_top, half_bottom, half_height):
    # a', b, a'', c: the order used in the CSV (runners a'->b and a''->c).
    # u runs along a row, v runs from the top edge to the bottom edge.
    top = center - half_height * v
    bottom = center + half_height * v
    return [top - half_top * u, bottom - half_bottom * u,
            top + half_top * u, bottom + half_bottom * u]


def write(path, lines, header=True):
    with open(path, "w") as f:
        if header:
            f.write(HEADER + "\n")
        f.write("\n".join(lines) + "\n")
    print(f"created {path} with {len(lines)} planes")


if __name__ == "__main__":
    os.makedirs("data-CSV", exist_ok=True)

    # the triangle moves along the z axis (from z=5 to z=94), so the video
    # "travels" through the tree trunk (plain rows, no header)
    write("data-CSV/trunk_sweep.csv",
          [f"50,10,{z},10,90,{z},90,90,{z}" for z in range(5, 95)], header=False)

    rotate = []
    for angle in np.linspace(0, np.pi, 120, endpoint=False):
        u = np.array([np.cos(angle), np.sin(angle), 0.0])    # horizontal direction
        rotate.append(row(trapezoid(CENTER, u, np.array([0, 0, 1.0]), 55, 65, 45)))
    write("data-CSV/trunk_rotate.csv", rotate)

    tilt = []
    for angle in np.linspace(0, np.pi, 120, endpoint=False):
        v = np.array([0.0, np.cos(angle), np.sin(angle)])    # turns around the x axis
        tilt.append(row(trapezoid(CENTER, np.array([1.0, 0, 0]), v, 45, 60, 50)))
    write("data-CSV/trunk_tilt.csv", tilt)
