# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
The system computes 2D cross-section images of a 3D volumetric scan (NRRD format) along arbitrary planes defined by the user, and exports them as a video, one frame per plane.

### 1.2 Users
Radiologists, physicians, medical researchers and developers of medical imaging software.

### 1.3 Usage
The system is a command-line tool. There is no graphical interface.

```bash
python Ex0.py <volume.nrrd> <planes.csv> <output.mp4>
```

## 2. Inputs and Outputs

### 2.1 Inputs
- **Volume file (.nrrd):** a 3D matrix of size sx × sy × sz (1 ≤ sx, sy, sz < 2^10).
  Each voxel is an unsigned integer of 8, 16 or 32 bits.
- **Planes file (.csv):** each row defines one plane.
  - 3 points (9 numbers: x1,y1,z1,x2,y2,z2,x3,y3,z3) = isosceles triangle
  - 4 points (12 numbers) = isosceles trapezoid

### 2.2 Outputs
- **Video file (.mp4):** one frame per CSV row, in the same order as the rows.
- All frames have the same fixed size. Smaller images are padded with black (0).
- Voxel values are normalized to the range 0-255 using the global minimum and
  maximum of the whole volume, computed once, so brightness is consistent
  across all frames.
### 3. Functional Requirements

### 3. Functional Requirements

- **FR1:** The system shall read a 3D volume from an NRRD file.
- **FR2:** The system shall compute the global minimum and maximum of the volume once.
- **FR3:** The system shall read a CSV file and parse each row as a plane.
- **FR3a:** The system shall determine the plane type by the number of values in a CSV row: 9 values = triangle (3 points), 12 values = trapezoid (4 points).
- **FR4:** For each plane, the system shall compute a 2D image by sampling the volume along the plane. A point outside the volume has value 0.
- **FR5:** The system shall normalize each image to 0-255 and pad it with black to the fixed frame size.
- **FR6:** The system shall write all images, in CSV order, to an MP4 file.
### 4. Non-Functional Requirements

- **NFR1 (Performance):** For a volume of size 500x500x500 voxels, the system shall generate at least 30 frames per second (target: 100 frames per second).
- **NFR2 (Stability):** The system shall not crash on valid input, and shall return a clear error message on invalid input.
- **NFR3 (Language):** The system shall be implemented in Python and run with the command: `python Ex0.py <volume.nrrd> <planes.csv> <output.mp4>`.
- **NFR4 (Efficiency):** Frame computation shall be vectorized (e.g., with NumPy) rather than using per-pixel loops, in order to meet NFR1.