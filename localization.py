from __future__ import annotations

import json
import locale as system_locale
import os
import sys
from pathlib import Path


DEFAULT_LOCALE = "en-US"


def _resource_root() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def _normalize_locale(value: str | None) -> str:
    if not value:
        return DEFAULT_LOCALE
    value = value.replace("_", "-")
    parts = value.split("-", 1)
    return parts[0].lower() if len(parts) == 1 else f"{parts[0].lower()}-{parts[1].upper()}"


class LocaleManager:
    def __init__(self) -> None:
        self.root = _resource_root() / "locales"
        self.manifest = self._read_json(self.root / "manifest.json")
        self.source_catalog = self._read_json(self.root / f"{DEFAULT_LOCALE}.json")
        self.source_keys = {value: key for key, value in self.source_catalog.items()}
        self.locale = DEFAULT_LOCALE
        self.catalog: dict[str, str] = {}

    @staticmethod
    def _read_json(path: Path) -> dict:
        try:
            data = json.loads(path.read_text("utf-8"))
            return data if isinstance(data, dict) else {}
        except (OSError, ValueError):
            return {}

    def available_locales(self) -> list[tuple[str, str]]:
        languages = self.manifest.get("languages", {})
        result: list[tuple[str, str]] = []
        for code, metadata in languages.items():
            if code == DEFAULT_LOCALE or (self.root / f"{code}.json").is_file():
                name = metadata.get("nativeName") or metadata.get("name") or code
                result.append((code, str(name)))
        return result or [(DEFAULT_LOCALE, "English (United States)")]

    def select(self, requested: str | None = None) -> str:
        requested = requested or os.environ.get("MESHMILL_LOCALE")
        if requested in (None, "", "system"):
            requested = system_locale.getlocale()[0]
        normalized = _normalize_locale(requested)
        candidates = [normalized, normalized.split("-", 1)[0]]
        available = {code for code, _name in self.available_locales()}
        self.locale = next((code for code in candidates if code in available), DEFAULT_LOCALE)
        self.catalog = (
            self._read_json(self.root / f"{self.locale}.json")
            if self.locale != DEFAULT_LOCALE
            else {}
        )
        return self.locale

    def translate(self, source: str) -> str:
        key = self.source_keys.get(source)
        if not key:
            return source
        translated = self.catalog.get(key)
        return translated if isinstance(translated, str) and translated else source


locale_manager = LocaleManager()


def tr(source: str) -> str:
    return locale_manager.translate(source)
