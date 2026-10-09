import struct
import threading
from pathlib import Path

import numpy as np

from out_of_core import IndexCancelled, build_index, index_matches, load_manifest


def write_binary_stl(path: Path, triangles: np.ndarray) -> None:
    with path.open("wb") as stream:
        stream.write(b"MeshMill test".ljust(80, b"\0"))
        stream.write(struct.pack("<I", len(triangles)))
        for triangle in triangles.astype("<f4"):
            stream.write(struct.pack("<3f", 0.0, 0.0, 1.0))
            stream.write(triangle.tobytes())
            stream.write(b"\0\0")


def test_index_partitions_every_triangle_and_reopens(tmp_path):
    source = tmp_path / "mesh.stl"
    triangles = np.array(
        [
            [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            [[10, 0, 0], [11, 0, 0], [10, 1, 0]],
            [[0, 10, 0], [1, 10, 0], [0, 11, 0]],
            [[10, 10, 10], [11, 10, 10], [10, 11, 10]],
        ],
        dtype=np.float32,
    )
    write_binary_stl(source, triangles)
    destination = tmp_path / "mesh.meshmill-index"

    created = build_index(
        source,
        destination,
        target_triangles_per_tile=1,
        block_triangles=2,
    )
    loaded = load_manifest(destination)

    assert loaded == created
    assert sum(tile.triangle_count for tile in loaded.tiles) == len(triangles)
    assert max(tile.triangle_count for tile in loaded.tiles) <= 65_536
    assert all(
        (destination / tile.relative_path).stat().st_size == tile.triangle_count * 50
        for tile in loaded.tiles
    )
    assert index_matches(source, loaded)
    assert all(tile.level <= loaded.max_depth for tile in loaded.tiles)


def test_index_detects_source_change(tmp_path):
    source = tmp_path / "mesh.stl"
    triangle = np.array([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], dtype=np.float32)
    write_binary_stl(source, triangle)
    destination = tmp_path / "mesh.meshmill-index"
    manifest = build_index(source, destination)

    with source.open("ab") as stream:
        stream.write(b"changed")

    assert not index_matches(source, manifest)


def test_cancel_does_not_publish_or_leave_staging(tmp_path):
    source = tmp_path / "mesh.stl"
    triangle = np.array([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], dtype=np.float32)
    write_binary_stl(source, np.repeat(triangle, 32, axis=0))
    destination = tmp_path / "mesh.meshmill-index"
    cancel = threading.Event()
    cancel.set()

    try:
        build_index(source, destination, cancel_event=cancel)
    except IndexCancelled:
        pass
    else:
        raise AssertionError("cancelled indexing unexpectedly completed")

    assert not destination.exists()
    assert not destination.with_name(destination.name + ".building").exists()


def test_parallel_analysis_matches_sequential_index(tmp_path):
    source = tmp_path / "parallel.stl"
    triangle = np.array([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], dtype=np.float32)
    triangles = np.repeat(triangle, 32_768, axis=0)
    triangles[:, :, 0] += np.arange(len(triangles), dtype=np.float32)[:, None]
    write_binary_stl(source, triangles)

    sequential = build_index(
        source,
        tmp_path / "sequential.meshmill-index",
        block_triangles=16_384,
        analysis_workers=1,
    )
    parallel = build_index(
        source,
        tmp_path / "parallel.meshmill-index",
        block_triangles=16_384,
        analysis_workers=2,
    )

    assert parallel.bounds == sequential.bounds
    assert parallel.max_depth == sequential.max_depth
    assert parallel.tiles == sequential.tiles
