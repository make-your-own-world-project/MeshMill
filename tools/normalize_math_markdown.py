"""Normalize Markdown math delimiters and detect unwrapped display equations."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TEX_COMMAND = re.compile(
    r"\\(?:frac|sum|sqrt|mathbf|operatorname|left|right|qquad|epsilon|theta|Delta|Vert|"
    r"lVert|rVert|cos|tan|arg|min|max|lfloor|rfloor|bar|mathbb|in|cap|varnothing|ge|le)\b"
)


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"(?m)^\\\[$", "$$", text)
    text = re.sub(r"(?m)^\\\]$", "$$", text)
    paragraphs = re.split(r"(\n\s*\n)", text)
    for index in range(0, len(paragraphs), 2):
        block = paragraphs[index]
        stripped = block.strip()
        if not stripped or stripped.startswith(("$$", "```", "|", "#", "- ", "* ", ">")):
            continue
        if "**Formula legend:**" in stripped or "$" in stripped or "`" in stripped:
            continue
        if not TEX_COMMAND.search(stripped) and "=" not in stripped:
            continue
        if not any(operator in stripped for operator in ("=", "<", ">")):
            continue
        paragraphs[index] = f"$$\n{stripped}\n$$"
    return "".join(paragraphs).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()
    failures: list[str] = []
    for path in args.paths:
        current = path.read_text("utf-8")
        expected = normalize(current)
        if current != expected:
            if args.fix:
                path.write_text(expected, "utf-8", newline="\n")
            else:
                failures.append(str(path))
    if failures:
        print("Math Markdown needs normalization:")
        print("\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
