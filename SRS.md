# Software Requirements Specification (SRS)

## 1. Introduction
The system takes a 3D scan (NRRD) and a list of planes (CSV), and creates a video where each frame is a 2D cross-section of the scan along one plane.
It is a command-line tool for doctors, researchers and developers of medical imaging software.

```bash
python Ex0.py <volume.nrrd> <planes.csv> <output.mp4>
```

## 2. Inputs and Outputs
- **Input 1, volume (.nrrd):** a 3D matrix of size sx × sy × sz (each below 2^10), with unsigned integer values of 8, 16 or 32 bits.
- **Input 2, planes (.csv):** one plane per row. 9 numbers = triangle, 12 numbers = trapezoid (3 or 4 points with x,y,z each).
- **Output (.mp4):** one frame per row, in the same order, all frames the same size.

## 3. Functional Requirements
- **FR1:** The system reads the volume and the planes.
- **FR2:** For each plane, it samples the volume along the plane to create a 2D image. A point outside the volume gets the value 0.
- **FR3:** It scales values to 0-255 using the minimum and maximum of the whole volume, and pads each image with black to a fixed size.
- **FR4:** It writes all images, in order, to the video file.

## 4. Non-Functional Requirements
- **NFR1 (Performance):** for a 500×500×500 volume, at least 30 frames per second (target: 100). Computation should use vectorized code (e.g. NumPy).
- **NFR2 (Stability):** no crash on valid input, and a clear error message on invalid input.

## 5. Error Handling
The whole CSV is checked before any frame is created. If a row is invalid, the system prints its row number and exits without creating a video.

**Errors (message and exit):**
- A file is missing, unreadable or empty, or the NRRD is not a 3D volume of unsigned integers.
- A CSV row has a wrong number of values, a non-number, or identical points.
- A triangle or trapezoid is not isosceles, or the 4 trapezoid points are not on one plane.
- The output file cannot be written.

**Not errors:**
- A plane partly or fully outside the volume: those points are 0 (black).
- Non-integer coordinates (e.g. 12.5): rounded to the nearest voxel.
- All voxels have the same value: all frames are black.
- A volume with a side of size 1: handled normally.
