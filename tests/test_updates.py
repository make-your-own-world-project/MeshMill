from __future__ import annotations

import hashlib
from pathlib import Path
from unittest.mock import patch

import pytest

import meshmill


def release_with(*names: str) -> dict:
    return {
        "version": "1.2.3",
        "release_url": "https://github.com/make-your-own-world/MeshMill/releases/tag/v1.2.3",
        "assets": [
            {"name": name, "url": "https://github.com/example", "digest": ""} for name in names
        ],
    }


def test_windows_update_selects_installer_not_portable_archive() -> None:
    release = release_with(
        "MeshMill-1.2.3-windows-x64-portable.zip",
        "MeshMill-1.2.3-windows-x64-setup.exe",
    )
    with (
        patch("meshmill.platform.system", return_value="Windows"),
        patch("meshmill.platform.machine", return_value="AMD64"),
    ):
        selected = meshmill.update_asset_for_current_platform(release)
    assert selected is not None
    assert selected["name"].endswith("-setup.exe")


@pytest.mark.parametrize(
    ("system", "asset"),
    [
        ("Darwin", "MeshMill-1.2.3-macos-universal.pkg"),
        ("Linux", "MeshMill-1.2.3-linux-x86_64.AppImage"),
    ],
)
def test_update_selects_native_installable_package(system: str, asset: str) -> None:
    with (
        patch("meshmill.platform.system", return_value=system),
        patch(
            "meshmill.platform.machine", return_value="arm64" if system == "Darwin" else "x86_64"
        ),
    ):
        assert meshmill.update_asset_for_current_platform(release_with(asset))["name"] == asset


def test_update_rejects_preview_archives() -> None:
    release = release_with("MeshMill-1.2.3-linux-x64.tar.gz", "MeshMill-1.2.3-macos-arm64.zip")
    for system in ("Linux", "Darwin"):
        with (
            patch("meshmill.platform.system", return_value=system),
            patch(
                "meshmill.platform.machine",
                return_value="arm64" if system == "Darwin" else "x86_64",
            ),
        ):
            assert meshmill.update_asset_for_current_platform(release) is None


def test_download_requires_release_digest(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="SHA-256"):
        meshmill.download_verified_update(
            {"url": "https://github.com/example/update.exe", "digest": ""},
            tmp_path / "update.exe",
        )


def test_download_verifies_digest_before_install(tmp_path: Path) -> None:
    content = b"verified installer"
    source = tmp_path / "source.exe"
    source.write_bytes(content)
    destination = tmp_path / "download.exe"
    asset = {
        "url": "https://github.com/example/update.exe",
        "digest": "sha256:" + hashlib.sha256(content).hexdigest(),
    }

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self, size: int) -> bytes:
            return source.open("rb").read() if not hasattr(self, "read_once") else b""

    response = Response()
    response.read_once = False

    def read_once(_size: int) -> bytes:
        if response.read_once:
            return b""
        response.read_once = True
        return content

    response.read = read_once
    with patch("meshmill.urlopen", return_value=response):
        result = meshmill.download_verified_update(asset, destination)
    assert result.read_bytes() == content
