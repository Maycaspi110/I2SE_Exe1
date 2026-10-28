# Algorithm: Plane Projection of a 3D Volume

## 1. Overview
The algorithm takes a 3D volume M and a plane defined by 3 or 4 points, and
returns a 2D image: the cross-section of the volume along that plane.
A video is created by running the algorithm once per plane and joining the images.

## 2. Inputs and Outputs
- **Input:** volume M (sx x sy x sz unsigned integers, 8/16/32 bit) and a plane:
  3 points (triangle) or 4 points (trapezoid). Both must be isosceles.
- **Output:** a 2D matrix E of size ceil(Dab) x ceil(Dbc), later normalized and
  resized to the fixed frame size.

## 3. Definitions
- **start1, start2:** the start points of the two "runners".
  Triangle (a, b, c): start1 = start2 = a.
  Trapezoid (a', a'', b, c): start1 = a', start2 = a''.
- **a1, a2:** the two runners. a1 walks from start1 to b, a2 walks from start2 to c.
- **Dab:** length of the side (the plane's height, in steps).
- **Dbc:** length of the bottom edge (the plane's width).
- **v1, v2:** unit vectors (length 1) along the two sides.
- **d12:** the current distance between a1 and a2 (the width of the current row).
- **dp:** unit vector from a1 to a2 (the direction along the row).

## 4. Design Decisions
1. **Rounding when sampling:** each point p is rounded to the nearest voxel.
   If the rounded point is outside the volume, its value is 0 (black).
2. **Image size:** height = ceil(Dab), width = ceil(Dbc). Pixels with no sampled
   value stay 0 (black). Writes outside matrix E (due to rounding) are ignored.
3. **Triangle vs. trapezoid:** the algorithm always works with two start points.
   A triangle is treated as a trapezoid whose start points coincide
   (a' = a'' = a), so a single implementation handles both cases.
4. **Isosceles validation:** the input plane must be isosceles (equal legs within
   a small tolerance). A plane that is not isosceles is rejected during CSV
   validation, before any frame is processed.
5. **Scaling to frame size:** the projection produces an image at natural scale
   (1 pixel = 1 voxel unit). A separate step then resizes it to the fixed frame
   size of 512x512 (a single constant), preserving the aspect ratio.
   Remaining area is padded with black (0).
6. **Normalization:** values are mapped to 0-255 using the global min and max of
   the whole volume, computed once. If min = max, the image is all black.

## 5. Steps
```
project(M, start1, start2, b, c):
    1. Dab = dist(start1, b)
       Dbc = dist(b, c)
    2. v1 = (b - start1) / Dab        # direction of the left side
       v2 = (c - start2) / Dab        # direction of the right side
    3. Create E: matrix of zeros, size ceil(Dab) x ceil(Dbc)
    4. a1 = start1, a2 = start2
    5. for y = 0 to ceil(Dab) - 1:
         a. a1 = a1 + v1
         b. a2 = a2 + v2
         c. d12 = dist(a1, a2)
         d. dp = (a2 - a1) / d12
         e. p = a1
         f. for x1 = 0 to d12:
              i.   q = round(p)
              ii.  v = M[q] if q is inside M, otherwise 0
              iii. x = (Dbc / 2) - (d12 / 2) + x1
              iv.  E[y][x] = v   (ignore if outside E)
              v.   p = p + dp
    6. return E
```

## 6. Full Pipeline
```
read NRRD -> compute global min/max (once) -> validate entire CSV ->
for each plane: project -> normalize -> resize to 512x512 -> write frame to MP4
```
If any CSV row is invalid, all errors are reported and no video is created.

## 7. Performance
A per-pixel Python loop is too slow (about 7.5 million pixels per second are needed
for 30 fps at 500x500). The projection is therefore vectorized with NumPy:

1. Build a grid of all pixel coordinates (y, x) of the output image.
2. For each pixel, compute its 3D point in the volume with array arithmetic:
   p = a1(y) + dp(y) * x1, for all pixels at once.
3. Round all points at once, and build a boolean mask of points inside the volume.
4. Fetch all values with a single NumPy fancy-indexing operation; points outside get 0.
5. Normalize and resize the whole image in one operation each.

The volume is loaded and its global min/max computed once, not per frame.
Target: at least 30 frames per second on a 500x500x500 volume.

## 8. Edge Cases
See the SRS document, section 5.