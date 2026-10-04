# Sample geometry

This directory contains an original composite development mesh and a smaller derivative. The
source originated from a 3D scan, then retained intentional layers of redundant geometry and varied
regional density. This makes it useful for testing density analysis, overlap handling, regional
operations, and competing optimization algorithms. People do not need a scanner to reproduce the
project's primary geometry experiments.

Both files are included as redistributable test data under the repository's
GPL-3.0-or-later license.

| Property | `original-scan.stl` | `sample-scan.stl` |
| --- | ---: | ---: |
| Storage | Git LFS | Normal Git |
| Format | Binary STL | Binary STL |
| Triangles | 4,126,315 | 249,999 |
| Vertices | 2,070,061 | approximately 127,000 |
| Dimensions | 831.659 × 371.834 × 479.154 | 831.181 × 371.135 × 479.146 |
| File size | 196.8 MiB | 11.9 MiB |

The smaller sample was produced from the original with MeshMill's Fast QEM algorithm and a target
of 250,000 triangles. The original exceeds GitHub's normal 100 MiB file limit and is therefore
tracked with Git LFS. Tagged releases publish it as a direct `.stl` download as well.

The geometry is provided as an algorithm-development, application-testing, and demonstration
fixture. Redundant or unusually dense regions may be intentional and should not be treated as
fixture defects. It is not a dimensional reference model.
