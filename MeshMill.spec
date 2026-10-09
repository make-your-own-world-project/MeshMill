# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(
    ['meshmill.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('LICENSE', '.'),
        ('README.md', '.'),
        ('ROADMAP.md', '.'),
        ('THIRD_PARTY_NOTICES.md', '.'),
        ('CUDA_EXCEPTION.md', '.'),
        ('docs/OUT_OF_CORE.md', 'docs'),
        ('docs/GPU_OUT_OF_CORE.md', 'docs'),
        ('assets/meshmill-mark.svg', 'assets'),
        ('assets/meshmill-logo.svg', 'assets'),
        ('locales/en-US.json', 'locales'),
    ],
    hiddenimports=[
        'unittest.mock',
        'vtkmodules.vtkInteractionStyle',
        'vtkmodules.vtkRenderingOpenGL2',
        'vtkmodules.vtkRenderingFreeType',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'pytest',
        'scipy',
        'cupy',
        'cupyx',
        'cupy_backends',
        'nvidia',
        'cupy_backends.cuda.libs.cudnn',
        'cupy_backends.cuda.libs.cutensor',
    ],
    noarchive=False,
    optimize=1,
)

# Qt uses the Windows ICU compatibility libraries. A developer machine may also
# expose unrelated ICU builds through PATH (for example, from PDF tooling), and
# PyInstaller can otherwise collect those DLLs while resolving Qt6Core. Bundling
# them makes Qt load the incompatible copy before the Windows implementation.
_foreign_icu_dlls = {'icuuc.dll', 'icudt78.dll'}
a.binaries = [entry for entry in a.binaries if entry[0].lower() not in _foreign_icu_dlls]

pyz = PYZ(a.pure)
gui = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MeshMill',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    version=os.path.join(SPECPATH, 'version_info.txt'),
    icon=os.path.join(SPECPATH, 'assets', 'meshmill.ico'),
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
cli = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MeshMillCLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    version=os.path.join(SPECPATH, 'version_info.txt'),
    icon=os.path.join(SPECPATH, 'assets', 'meshmill.ico'),
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    gui,
    cli,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MeshMill',
)
