# -*- mode: python ; coding: utf-8 -*-
import os
import sys


project_root = os.path.dirname(os.path.abspath(SPECPATH))
version = os.environ.get("MESHMILL_BUILD_VERSION", "0.0.0-preview")
bundle_version = version.split("-", 1)[0]

a = Analysis(
    [os.path.join(project_root, "meshmill.py")],
    pathex=[project_root],
    binaries=[],
    datas=[
        (os.path.join(project_root, "LICENSE"), "."),
        (os.path.join(project_root, "README.md"), "."),
        (os.path.join(project_root, "ROADMAP.md"), "."),
        (os.path.join(project_root, "THIRD_PARTY_NOTICES.md"), "."),
        (os.path.join(project_root, "docs", "OUT_OF_CORE.md"), "docs"),
        (os.path.join(project_root, "docs", "PLATFORM_TESTING.md"), "docs"),
        (os.path.join(project_root, "assets", "meshmill-mark.svg"), "assets"),
        (os.path.join(project_root, "assets", "meshmill-logo.svg"), "assets"),
        (os.path.join(project_root, "locales"), "locales"),
    ],
    hiddenimports=[
        "vtkmodules.vtkInteractionStyle",
        "vtkmodules.vtkRenderingOpenGL2",
        "vtkmodules.vtkRenderingFreeType",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "pandas", "scipy"],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MeshMill",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="MeshMill",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="MeshMill.app",
        icon=None,
        bundle_identifier="org.makeyourownworld.meshmill",
        version=bundle_version,
        info_plist={
            "CFBundleDisplayName": "MeshMill",
            "CFBundleName": "MeshMill",
            "CFBundleShortVersionString": bundle_version,
            "CFBundleVersion": bundle_version,
            "NSHighResolutionCapable": True,
            "NSPrincipalClass": "NSApplication",
            "NSAppleScriptEnabled": False,
            "CFBundleDocumentTypes": [
                {
                    "CFBundleTypeName": "STL mesh",
                    "CFBundleTypeRole": "Editor",
                    "LSHandlerRank": "Alternate",
                    "LSItemContentTypes": ["public.standard-tesselated-geometry-format"],
                    "CFBundleTypeExtensions": ["stl"],
                }
            ],
        },
    )
