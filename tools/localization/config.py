from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / ".localization-work"
PORT = 8774

DOCUMENTS = (
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "RELEASING.md",
    "ROADMAP.md",
    "SECURITY.md",
    "SUPPORT.md",
    "THIRD_PARTY_NOTICES.md",
    "docs/ALGORITHM_TESTING.md",
    "docs/OUT_OF_CORE.md",
    "docs/TROUBLESHOOTING.md",
)
UI_CATALOG = ROOT / "locales" / "en-US.json"

LANGUAGES = {
    "en-US": "English (United States)",
    "ar": "Arabic",
    "bn": "Bengali",
    "de": "German",
    "el": "Greek",
    "es": "Spanish",
    "fa": "Persian",
    "fr": "French",
    "ga": "Irish",
    "hi": "Hindi",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sr": "Serbian",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Simplified Chinese",
}

RTL_LANGUAGES = {"ar", "fa", "ur"}
PROTECTED_TERMS = (
    "MeshMill",
    "STL",
    "GPU",
    "CPU",
    "RAM",
    "OpenGL",
    "Python",
    "Node.js",
    "GitHub",
    "Git LFS",
    "Windows",
    "Linux",
    "macOS",
    "Fast QEM",
    "Ctrl+X",
    "Ctrl+C",
    "Ctrl+Space",
)
