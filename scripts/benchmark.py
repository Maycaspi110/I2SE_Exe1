import time
import numpy as np
from src.slicer import project_plane

# 500x500x500 volume of random bytes (125 MB)
volume = np.random.randint(0, 256, (500, 500, 500), dtype=np.uint8)

frames = 10
start = time.time()
for i in range(frames):
    z = 100 + i * 20
    project_plane(volume, [250, 50, z], [250, 50, z],
                  [150, 400, z], [350, 400, z])
seconds = time.time() - start
print(f"{frames / seconds:.1f} frames per second")