"""Validate UI catalogs and localized-document layout."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import DOCUMENTS, LANGUAGES, ROOT, UI_CATALOG


def load_object(path: Path) -> dict[str, str]:
    try:
        value = json.loads(path.read_text("utf-8"))
    except (OSError, ValueError) as error:
        raise SystemExit(f"Invalid locale catalog {path}: {error}") from error
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(text, str) for key, text in value.items()
    ):
        raise SystemExit(f"Locale catalog must be a string-to-string object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-only",
        action="store_true",
        help="validate only the English source catalog for an English-only release",
    )
    arguments = parser.parse_args()
    source = load_object(UI_CATALOG)
    if arguments.source_only:
        if not source:
            raise SystemExit("English source catalog is empty")
        print(f"English source catalog valid: {len(source)} UI strings")
        return 0
    failures: list[str] = []
    locale_root = ROOT / "locales"
    for path in sorted(locale_root.glob("*.json")):
        if path.name in {"manifest.json", UI_CATALOG.name}:
            continue
        catalog = load_object(path)
        locale = path.stem
        if locale not in LANGUAGES:
            failures.append(f"unsupported locale catalog: {path.name}")
        missing = source.keys() - catalog.keys()
        extra = catalog.keys() - source.keys()
        empty = {key for key, text in catalog.items() if not text.strip()}
        if missing:
            failures.append(f"{path.name}: {len(missing)} missing keys")
        if extra:
            failures.append(f"{path.name}: {len(extra)} unknown keys")
        if empty:
            failures.append(f"{path.name}: {len(empty)} empty values")
        docs = ROOT / "docs" / "locales" / locale
        if docs.exists():
            absent = [name for name in DOCUMENTS if not (docs / name).is_file()]
            if absent:
                failures.append(f"docs/{locale}: missing {', '.join(absent)}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Locale structure valid: {len(source)} English UI strings, {len(LANGUAGES)} locales")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
