# Third-party software

MeshMill depends on the following software. These components retain their own licenses and
copyright notices.

| Component | Version | License |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Python Software Foundation License |
| [NumPy](https://numpy.org/) | 2.5.3 | BSD-3-Clause and bundled permissive licenses |
| [fast-simplification](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | BSD-3-Clause |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | LGPL-3.0-only, GPL-2.0-only, or GPL-3.0-only |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | LGPL-3.0-only, GPL-2.0-only, or GPL-3.0-only |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0-or-later with a bootloader exception |
| [CuPy](https://cupy.dev/) | 13.6.0 | MIT and bundled permissive licenses |
| [fastrlock](https://github.com/scoder/fastrlock) | 0.8.3 | MIT |
| [NVIDIA CUDA Runtime](https://developer.nvidia.com/cuda-toolkit) | 12.4.127 | NVIDIA CUDA Toolkit EULA |
| [NVIDIA NVRTC](https://docs.nvidia.com/cuda/nvrtc/) | 12.0.140 | NVIDIA CUDA Toolkit EULA |

The Windows bundle distributes PySide6 and Shiboken6 under their GPL-3.0 option, consistent
with MeshMill's GPL-3.0-or-later license. NumPy wheels contain additional permissively licensed
components; their notices are included in the installed package metadata and should be retained
when redistributing a modified binary bundle.

CuPy and `fastrlock` are used by the optional Depth Adaptive QEM computation path. Their complete
license texts are retained in the packaged Python metadata under `_internal/cuda_runtime`.

The Windows installer and portable archive include unmodified CUDA Runtime and NVRTC binary
components identified as redistributable in Attachment A of the
[NVIDIA CUDA Toolkit EULA](https://docs.nvidia.com/cuda/eula/). They are stored in MeshMill's private
`_internal/cuda_runtime` directory and are accessed only by MeshMill. NVIDIA components remain
proprietary NVIDIA software, are not licensed under the GNU GPL, and are intended for use with
compatible NVIDIA hardware. Complete NVIDIA license texts are retained at:

- `_internal/cuda_runtime/nvidia_cuda_runtime_cu12-12.4.127.dist-info/License.txt`
- `_internal/cuda_runtime/nvidia_cuda_nvrtc_cu12-12.0.140.dist-info/License.txt`

MeshMill's permission to interoperate with these separately licensed components is described in
[`CUDA_EXCEPTION.md`](CUDA_EXCEPTION.md). No NVIDIA driver, system-wide CUDA Toolkit, background
service, or scheduled task is installed.
