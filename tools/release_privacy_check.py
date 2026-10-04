"""Reject common private-data and work-session artifacts before publication."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".localization-work", "__pycache__", "build", "dist", "release"}
TEXT_SUFFIXES = {
    ".cfg", ".css", ".ini", ".iss", ".json", ".md", ".ps1", ".py", ".svg",
    ".toml", ".txt", ".yml", ".yaml",
}
FORBIDDEN_FILE_NAMES = {
    "browser-progress.json", "orientation-session.jsonl", "progress.json",
    "translation-cache.json",
}
PATTERNS = {
    "email address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "Windows user profile path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+"),
    "macOS user profile path": re.compile(r"/Users/[^/\s]+"),
    "Linux user profile path": re.compile(r"/home/[^/\s]+"),
    "Codex workspace path": re.compile(r"(?i)(?:Documents[\\/]Codex|\.codex[\\/])"),
    "translation audit artifact": re.compile(
        r"(?i)(?:BROWSER-PROGRESS\.json|translation-cache\.json|batch-results[\\/])"
    ),
}
PNG_PRIVATE_CHUNKS = {b"tEXt", b"zTXt", b"iTXt", b"eXIf"}


def publishable_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not (set(path.relative_to(ROOT).parts) & SKIP_PARTS)
    ]


def check_png(path: Path, failures: list[str]) -> None:
    data = path.read_bytes()
    offset = 8
    while offset + 12 <= len(data):
        length = int.from_bytes(data[offset : offset + 4], "big")
        kind = data[offset + 4 : offset + 8]
        if kind in PNG_PRIVATE_CHUNKS:
            failures.append(f"{path.relative_to(ROOT)}: metadata chunk {kind.decode('ascii')}")
        offset += 12 + length


def check_commit_emails(failures: list[str]) -> None:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--format=%ae"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return
    for email in {line.strip() for line in result.stdout.splitlines() if line.strip()}:
        if not email.casefold().endswith("@users.noreply.github.com"):
            failures.append("Git history contains an author email that is not a GitHub no-reply address")
            break


def main() -> int:
    failures: list[str] = []
    for path in publishable_files():
        relative = path.relative_to(ROOT)
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.name.casefold() in FORBIDDEN_FILE_NAMES:
            failures.append(f"{relative}: work-session artifact filename")
        if path.suffix.casefold() == ".png":
            check_png(path, failures)
        if path.suffix.casefold() not in TEXT_SUFFIXES:
            continue
        text = path.read_text("utf-8", errors="replace")
        for label, pattern in PATTERNS.items():
            if label == "translation audit artifact" and relative.parts[:2] == (
                "tools",
                "localization",
            ):
                continue
            if pattern.search(text):
                failures.append(f"{relative}: {label}")
    check_commit_emails(failures)
    if failures:
        raise SystemExit("Privacy check failed:\n" + "\n".join(f"- {item}" for item in failures))
    print("Privacy check passed: no private email, user path, session artifact, or image metadata found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
