"""Create a deterministic, isolated browser-translation queue for MeshMill."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from config import DOCUMENTS, LANGUAGES, PORT, PROTECTED_TERMS, ROOT, UI_CATALOG, WORK

TOKEN_RE = re.compile(
    r"`[^`\n]+`|https?://[^\s)>]+|(?:[A-Za-z]:[\\/])?[^\s()]+\.(?:md|stl|exe|json|toml|ps1)|"
    + "|".join(re.escape(term) for term in sorted(PROTECTED_TERMS, key=len, reverse=True))
)
FENCE_RE = re.compile(r"^\s*```")
TABLE_RULE_RE = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$")
LINK_REFERENCE_RE = re.compile(r"^\s*\[[^\]]+\]:\s+\S+")
NAVIGATION_START = "<!-- localization-navigation:start -->"
NAVIGATION_END = "<!-- localization-navigation:end -->"
PREFIX_RE = re.compile(r"^(\s*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s+)?)")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protect(text: str) -> tuple[str, dict[str, str]]:
    tokens: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        marker = f"ZXQ{len(tokens):04d}QXZ"
        tokens[marker] = match.group(0)
        return marker

    return TOKEN_RE.sub(replace, text), tokens


def markdown_passages(text: str) -> list[dict[str, object]]:
    passages: list[dict[str, object]] = []
    fenced = False
    navigation = False
    offset = 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        newline = line[len(body) :]
        if body.strip() == NAVIGATION_START:
            navigation = True
            offset += len(line)
            continue
        if body.strip() == NAVIGATION_END:
            navigation = False
            offset += len(line)
            continue
        if FENCE_RE.match(body):
            fenced = not fenced
            offset += len(line)
            continue
        if navigation or fenced or not body.strip() or TABLE_RULE_RE.match(body) or LINK_REFERENCE_RE.match(body):
            offset += len(line)
            continue
        prefix = PREFIX_RE.match(body).group(1)
        content = body[len(prefix) :]
        if not content.strip():
            offset += len(line)
            continue
        protected, tokens = protect(content)
        passages.append(
            {
                "start": offset + len(prefix),
                "end": offset + len(body),
                "source": content,
                "protected_source": protected,
                "tokens": tokens,
                "newline": newline,
            }
        )
        offset += len(line)
    return passages


def main() -> int:
    missing = [name for name in DOCUMENTS if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit(f"Missing authoritative documents: {', '.join(missing)}")
    if not UI_CATALOG.is_file():
        raise SystemExit("Run extract_ui_catalog.py and review locales/en.json first.")

    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "batch-results").mkdir(exist_ok=True)
    (WORK / "staging").mkdir(exist_ok=True)
    cache_path = WORK / "translation-cache.json"
    cache = json.loads(cache_path.read_text("utf-8")) if cache_path.exists() else {}
    ui = json.loads(UI_CATALOG.read_text("utf-8"))
    manifest = {
        "port": PORT,
        "documents": {name: digest(ROOT / name) for name in DOCUMENTS},
        "ui_catalog": digest(UI_CATALOG),
        "shared_images": {
            str(path.relative_to(ROOT)).replace("\\", "/"): digest(path)
            for path in sorted((ROOT / "docs" / "images").glob("*"))
            if path.is_file()
        },
        "languages": LANGUAGES,
    }
    (WORK / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", "utf-8"
    )

    sources: list[dict[str, object]] = []
    for document_index, name in enumerate(DOCUMENTS):
        text = (ROOT / name).read_text("utf-8")
        for passage_index, passage in enumerate(markdown_passages(text)):
            sources.append(
                {
                    "kind": "document",
                    "document": name,
                    "document_index": document_index,
                    "passage_index": passage_index,
                    **passage,
                }
            )
    for passage_index, (key, value) in enumerate(ui.items()):
        protected, tokens = protect(value)
        sources.append(
            {
                "kind": "ui",
                "ui_key": key,
                "document_index": len(DOCUMENTS),
                "passage_index": passage_index,
                "source": value,
                "protected_source": protected,
                "tokens": tokens,
            }
        )

    queue = []
    target_languages = [locale for locale in LANGUAGES if locale != "en-US"]
    for language_index, locale in enumerate(target_languages):
        for source in sources:
            key = locale + "\0" + str(source["source"])
            if key not in cache:
                queue.append(
                    {
                        "locale": locale,
                        "language_index": language_index,
                        "key": key,
                        **source,
                    }
                )
    queue.sort(key=lambda row: (row["language_index"], row["document_index"], row["passage_index"]))
    (WORK / "queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", "utf-8")
    if not cache_path.exists():
        cache_path.write_text("{}\n", "utf-8")
    progress = {
        "status": "prepared",
        "port": PORT,
        "languages": len(target_languages),
        "documents": len(DOCUMENTS),
        "ui_strings": len(ui),
        "missing_passages": len(queue),
        "source_characters": sum(len(str(row["source"])) for row in queue),
        "translation_started": False,
    }
    (WORK / "progress.json").write_text(json.dumps(progress, indent=2) + "\n", "utf-8")
    print(json.dumps(progress, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
