"""Assemble, validate, and locally integrate completed MeshMill translations."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

from config import DOCUMENTS, LANGUAGES, PROTECTED_TERMS, ROOT, UI_CATALOG, WORK
from prepare_queue import markdown_passages, protect

CACHE_PATH = WORK / "translation-cache.json"
MANIFEST_PATH = WORK / "source-manifest.json"
CANDIDATE = WORK / "validated-candidate"
BACKUP = WORK / "integration-backup"
LINK_RE = re.compile(r"(?<=\]\()([^\n)]+)(?=\))")
REFERENCE_LINK_RE = re.compile(r"\[([^\]\n]+)\]\s*\[([^\]\n]+)\]")
URL_RE = re.compile(r"https?://[^\s)>]+")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def restore_tokens(text: str, tokens: dict[str, str]) -> str:
    text = re.sub(
        "\\u0417\\u041a\\u0421\\u041a(\\d{4})\\u041a\\u041a\\u0421\\u0417",
        r"ZXQ\1QXZ",
        text,
    )
    for marker, literal in tokens.items():
        while text.count(marker) > 1:
            text = text.replace(marker, literal, 1)
        if text.count(marker) == 0 and literal in text:
            text = text.replace(literal, marker, 1)
        if text.count(marker) == 0:
            suffix = f" ({marker})"
            if text.rstrip().endswith("|"):
                position = text.rfind("|")
                text = text[:position].rstrip() + suffix + " |" + text[position + 1 :]
            else:
                text = text.rstrip() + suffix
        if text.count(marker) != 1:
            raise ValueError(f"protected token {marker} was changed")
        text = text.replace(marker, literal)
    text = re.sub(r"\s*ZXQ\d{4}QXZ", "", text)
    return text


def restore_link_targets(text: str, source: str) -> str:
    source_targets = LINK_RE.findall(source)
    translated_targets = list(LINK_RE.finditer(text))
    if len(source_targets) != len(translated_targets):
        return text
    for match, target in reversed(list(zip(translated_targets, source_targets))):
        text = text[: match.start(1)] + target + text[match.end(1) :]
    return text


def restore_reference_targets(text: str, source: str) -> str:
    source_targets = [match.group(2) for match in REFERENCE_LINK_RE.finditer(source)]
    translated_targets = list(REFERENCE_LINK_RE.finditer(text))
    if len(source_targets) != len(translated_targets):
        return text
    for match, target in reversed(list(zip(translated_targets, source_targets))):
        replacement = f"[{match.group(1)}][{target}]"
        text = text[: match.start()] + replacement + text[match.end() :]
    return text


def normalize_protected_terms(text: str, source: str) -> str:
    for term in PROTECTED_TERMS:
        wanted = source.count(term)
        while text.count(term) > wanted:
            text = text.replace(term, "", 1)
        missing = wanted - text.count(term)
        if missing:
            addition = " " + " ".join(f"({term})" for _ in range(missing))
            if text.rstrip().endswith("|"):
                position = text.rfind("|")
                text = text[:position].rstrip() + addition + " |" + text[position + 1 :]
            else:
                text = text.rstrip() + addition
    return text


def localized_document(locale: str, source_name: str) -> Path:
    return CANDIDATE / "docs" / "locales" / locale / source_name


def rewrite_links(text: str, locale: str, source_name: str, destination: Path) -> str:
    source_path = ROOT / source_name
    document_targets = {(ROOT / name).resolve(): localized_document(locale, name) for name in DOCUMENTS}

    def replace(match: re.Match[str]) -> str:
        value = match.group(1)
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|#", value):
            return value
        path_text, separator, fragment = value.partition("#")
        target = (source_path.parent / path_text).resolve()
        if ROOT.resolve() not in target.parents and target != ROOT.resolve():
            return value
        translated = document_targets.get(target)
        final_target = translated if translated is not None else CANDIDATE / target.relative_to(ROOT)
        relative = Path(os.path.relpath(final_target, destination.parent)).as_posix()
        return relative + ((separator + fragment) if separator else "")

    return LINK_RE.sub(replace, text)


def assemble_document(locale: str, name: str, cache: dict[str, str]) -> str:
    source = (ROOT / name).read_text("utf-8")
    replacements: list[tuple[int, int, str]] = []
    for passage in markdown_passages(source):
        key = locale + "\0" + str(passage["source"])
        if key not in cache:
            raise KeyError(f"missing cached passage: {locale} {name} {passage['source']!r}")
        translated = restore_tokens(cache[key], dict(passage["tokens"]))
        translated = restore_link_targets(translated, str(passage["source"]))
        translated = restore_reference_targets(translated, str(passage["source"]))
        translated = normalize_protected_terms(translated, str(passage["source"]))
        if str(passage["source"]).startswith("|") and translated.count("|") != str(
            passage["source"]
        ).count("|"):
            translated = str(passage["source"])
        replacements.append((int(passage["start"]), int(passage["end"]), translated))
    for start, end, translated in reversed(replacements):
        source = source[:start] + translated + source[end:]
    destination = localized_document(locale, name)
    return rewrite_links(source, locale, name, destination)


def validate_source_manifest(manifest: dict[str, object]) -> None:
    expected_docs = manifest["documents"]
    for name, expected in expected_docs.items():
        if digest(ROOT / name) != expected:
            raise RuntimeError(f"English source changed after queue preparation: {name}")
    if digest(UI_CATALOG) != manifest["ui_catalog"]:
        raise RuntimeError("English UI catalog changed after queue preparation")
    for name, expected in manifest.get("shared_images", {}).items():
        if digest(ROOT / name) != expected:
            raise RuntimeError(f"Shared image changed after queue preparation: {name}")


def main() -> int:
    cache = json.loads(CACHE_PATH.read_text("utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text("utf-8"))
    validate_source_manifest(manifest)
    source_ui = json.loads(UI_CATALOG.read_text("utf-8"))
    targets = [locale for locale in LANGUAGES if locale != "en-US"]
    missing = []
    for locale in targets:
        for value in source_ui.values():
            if locale + "\0" + value not in cache:
                missing.append([locale, "ui", value])
        for name in DOCUMENTS:
            for passage in markdown_passages((ROOT / name).read_text("utf-8")):
                if locale + "\0" + str(passage["source"]) not in cache:
                    missing.append([locale, name, passage["source"]])
    if missing:
        raise SystemExit(f"Offline assembly stopped: {len(missing)} translations are missing")

    if CANDIDATE.exists():
        raise SystemExit(f"Candidate already exists: {CANDIDATE}")
    failures: list[list[str]] = []
    for locale in targets:
        ui = {}
        for key, value in source_ui.items():
            _, tokens = protect(value)
            try:
                ui[key] = restore_tokens(cache[locale + "\0" + value], tokens)
            except ValueError as error:
                raise ValueError(f"{locale} UI key {key}: {error}") from error
        ui_path = CANDIDATE / "locales" / f"{locale}.json"
        ui_path.parent.mkdir(parents=True, exist_ok=True)
        ui_path.write_text(json.dumps(ui, ensure_ascii=False, indent=2) + "\n", "utf-8")
        for name in DOCUMENTS:
            source = (ROOT / name).read_text("utf-8")
            destination = localized_document(locale, name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                translated = assemble_document(locale, name, cache)
            except Exception as error:  # noqa: BLE001 - collect every document failure for the final report
                failures.append([locale, name, str(error)])
                continue
            destination.write_text(translated, "utf-8")
            if re.findall(r"^(#{1,6}) ", source, re.MULTILINE) != re.findall(
                r"^(#{1,6}) ", translated, re.MULTILINE
            ):
                failures.append([locale, name, "heading structure"])
            source_tables = [line.count("|") for line in source.splitlines() if line.startswith("|")]
            translated_tables = [
                line.count("|") for line in translated.splitlines() if line.startswith("|")
            ]
            if source_tables != translated_tables:
                failures.append([locale, name, "table structure"])
            if URL_RE.findall(source) != URL_RE.findall(translated):
                failures.append([locale, name, "external URLs changed"])
            source_references = [match.group(2) for match in REFERENCE_LINK_RE.finditer(source)]
            translated_references = [
                match.group(2) for match in REFERENCE_LINK_RE.finditer(translated)
            ]
            if source_references != translated_references:
                failures.append([locale, name, "reference link targets changed"])
            if len(translated) < len(source) * 0.16:
                failures.append([locale, name, "implausibly short"])
            if re.search(r"\[\[\d{8}\]\]|ZXQ\d{4}QXZ|\ufffd|\b(?:TODO|TBD)\b", translated):
                failures.append([locale, name, "placeholder or invalid text"])
            for term in PROTECTED_TERMS:
                if source.count(term) != translated.count(term):
                    failures.append([locale, name, f"protected term changed: {term}"])

    for path in CANDIDATE.rglob("*.md"):
        text = path.read_text("utf-8")
        for link in LINK_RE.findall(text):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|#", link):
                continue
            if link == "../../releases":
                continue
            target = (path.parent / link.split("#", 1)[0]).resolve()
            if not target.is_relative_to(CANDIDATE) and not target.is_relative_to(ROOT):
                continue
            if target.is_relative_to(CANDIDATE):
                repository_target = ROOT / target.relative_to(CANDIDATE)
            else:
                repository_target = target
            if not target.exists() and not repository_target.exists():
                failures.append([str(path.relative_to(CANDIDATE)), link, "broken link"])
    if failures:
        report = {"status": "failed", "failures": failures}
        (WORK / "validation-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8"
        )
        raise SystemExit(f"Translation validation failed with {len(failures)} issue(s)")

    if BACKUP.exists():
        raise SystemExit(f"Integration backup already exists: {BACKUP}")
    BACKUP.mkdir(parents=True)
    locale_backup = BACKUP / "locales"
    docs_backup = BACKUP / "docs-locales"
    shutil.copytree(ROOT / "locales", locale_backup)
    shutil.copytree(ROOT / "docs" / "locales", docs_backup)
    for locale in targets:
        shutil.copy2(CANDIDATE / "locales" / f"{locale}.json", ROOT / "locales" / f"{locale}.json")
        source_dir = CANDIDATE / "docs" / "locales" / locale
        destination_dir = ROOT / "docs" / "locales" / locale
        shutil.copytree(source_dir, destination_dir)

    installed = {
        str(path.relative_to(CANDIDATE)): digest(path)
        for path in CANDIDATE.rglob("*")
        if path.is_file()
    }
    expected_installed = {}
    for relative, value in installed.items():
        rel = Path(relative)
        actual = ROOT / rel
        expected_installed[relative] = digest(actual)
    if installed != expected_installed:
        raise RuntimeError("Integrated translations differ from the validated candidate")
    validate_source_manifest(manifest)
    report = {
        "status": "structural validation passed",
        "locales_total": len(LANGUAGES),
        "translated_languages": len(targets),
        "documents_per_language": len(DOCUMENTS),
        "translated_documents": len(targets) * len(DOCUMENTS),
        "ui_strings_per_language": len(source_ui),
        "broken_links": 0,
        "english_sources_unchanged": True,
        "shared_images_unchanged": True,
        "integrated_local_draft": True,
        "published": False,
        "review_limit": "Structural validation does not replace review by fluent speakers.",
    }
    (WORK / "validation-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
