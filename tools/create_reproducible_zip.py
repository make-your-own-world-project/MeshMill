"""Create a ZIP archive without leaking source-file timestamps."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def create_archive(source: Path, destination: Path) -> None:
    source = source.resolve()
    destination = destination.resolve()
    root_name = source.name

    with ZipFile(destination, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source.rglob("*"), key=lambda item: item.as_posix().casefold()):
            if not path.is_file():
                continue
            relative = path.relative_to(source).as_posix()
            info = ZipInfo(f"{root_name}/{relative}", ARCHIVE_TIMESTAMP)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.create_system = 3
            with path.open("rb") as source_file, archive.open(info, "w") as target_file:
                while chunk := source_file.read(1024 * 1024):
                    target_file.write(chunk)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    if not args.source.is_dir():
        parser.error(f"source directory does not exist: {args.source}")

    args.destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.destination.with_suffix(args.destination.suffix + ".tmp")
    try:
        create_archive(args.source, temporary)
        os.replace(temporary, args.destination)
    finally:
        temporary.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
