# Software Requirements Specification (SRS)

## 1. Introduction
The system takes a 3D scan (NRRD file) and a list of planes (CSV file), and creates a video. Each frame in the video is a 2D cross-section of the scan along one plane.

The system is a command-line tool, with no graphical interface. It is meant for doctors, medical researchers and developers of medical imaging software.

```bash
python Ex0.py <volume.nrrd> <planes.csv> <output.mp4>
```

### 1.1 Scope
- **In scope:** reading an NRRD volume and a CSV of planes, computing the cross-section images, and writing them to an MP4 video.
- **Out of scope:** a graphical interface, a 3D viewer, and editing or saving the volume.

### 1.2 Definitions
| Term | Meaning |
|------|---------|
| Voxel | One cell of the 3D matrix, M[x][y][z] |
| NRRD | File format that stores a 3D scan (for example an MRI) |
| Plane | A flat surface in 3D, given by an isosceles triangle (3 points) or an isosceles trapezoid (4 points) |
| Frame | One 2D image in the video, created from one plane |
| FPS | Frames per second |

### 1.3 Assumptions and Constraints
- The system is written in Python, using NumPy for the computation and an MP4 library (for example OpenCV) for the video.
- The whole volume fits in memory (a 500×500×500 byte volume is about 125 MB).
- Coordinates in the CSV are in voxel units, in the order x,y,z, where x,y,z are the axes of the matrix M.

## 2. Inputs and Outputs
**Inputs**
- **Volume (.nrrd):** a 3D matrix of size sx × sy × sz (each from 1 up to 2^10 - 1). Each value is an unsigned integer of 8, 16 or 32 bits.
- **Planes (.csv):** each row is one plane, given by 3 or 4 points with x,y,z each.
  - 9 numbers = isosceles triangle.
  - 12 numbers = isosceles trapezoid.

**Output**
- **Video (.mp4):** one frame per CSV row, in the same order as the rows. The video is grayscale, at 30 FPS. All frames have the same fixed size: the largest width and the largest height among all the planes.
- **Frame size:** the projection creates an image at natural scale (1 pixel = 1 voxel unit). A separate step pads it with black (0), centered, up to the frame size. The image is never resized, so every pixel is a real value from the scan.

## 3. Functional Requirements
- **FR1:** The system reads the volume from the NRRD file and the planes from the CSV file.
- **FR2:** For each plane, the system samples the volume along the plane and creates a 2D image. A point outside the volume gets the value 0.
- **FR3:** Each sample takes the value of the nearest voxel (no interpolation).
- **FR4:** The system scales the values to 0-255, using the minimum and maximum of the whole volume (computed once), so the brightness is the same in all frames. Results are clipped to 0-255, so a point outside the volume (value 0), even when it is below the volume minimum, stays black.
- **FR5:** The system pads each image with black (0), centered, up to the frame size, without resizing it.
- **FR6:** The system writes all images, in order, to the MP4 file.

## 4. Non-Functional Requirements
- **NFR1 (Performance):** for a 500×500×500 volume, the system creates at least 30 frames per second (target: 100).
- **NFR2 (Efficiency):** the computation uses vectorized code (for example NumPy) and not loops over single pixels, in order to meet NFR1.
- **NFR3 (Stability):** the system does not crash on valid input, and prints a clear error message on invalid input.

## 5. Edge Cases and Error Handling
The whole CSV is checked before any frame is created. If a row is invalid, the system prints all the invalid row numbers and exits without creating a video. No row is skipped, so the video always has one frame per CSV row.

**Errors (print a message and exit):**
- The command line does not have exactly 3 arguments (print the usage line).
- A file is missing, unreadable or empty.
- The NRRD file is not a 3D volume of unsigned integers.
- A CSV row has a wrong number of values (not 9 or 12), or a value that is not a number.
- A CSV row has two identical points (the plane is degenerate).
- The plane is not isosceles: in a triangle `dist(a,b) != dist(a,c)`, and in a trapezoid the two legs have different lengths.
- The 4 points of a trapezoid are not on one plane.
- The output file cannot be written.

**Not errors:**
- A plane that is partly or fully outside the volume: the points outside get 0 (black).
- Non-integer coordinates (for example 12.5): rounded to the nearest voxel.
- All voxels have the same value (min = max): all frames are black, so there is no division by zero.
- A volume with a side of size 1: handled like any other volume.
