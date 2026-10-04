"""Extract stable, user-visible English literals for localization review."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

from config import ROOT, UI_CATALOG

VISIBLE_CALLS = {
    "QCheckBox",
    "QLabel",
    "QPushButton",
    "field_label",
    "addItem",
    "addItems",
    "addRow",
    "about",
    "critical",
    "getOpenFileName",
    "getSaveFileName",
    "setInformativeText",
    "setText",
    "setToolTip",
    "setWindowTitle",
}


def slug(text: str) -> str:
    key = re.sub(r"[^a-z0-9]+", ".", text.lower()).strip(".")
    return key[:72] or "text"


def strings(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, (ast.List, ast.Tuple)):
        result: list[str] = []
        for item in node.elts:
            result.extend(strings(item))
        return result
    if isinstance(node, ast.Dict):
        result: list[str] = []
        for item in node.values:
            result.extend(strings(item))
        return result
    if isinstance(node, ast.IfExp):
        return strings(node.body) + strings(node.orelse)
    return []


def main() -> int:
    source = ROOT / "meshmill.py"
    tree = ast.parse(source.read_text("utf-8"), filename=str(source))
    values: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == "help_text" for target in targets):
                values.extend(strings(node.value))
        if not isinstance(node, ast.Call):
            continue
        name = ""
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        if name not in VISIBLE_CALLS:
            continue
        for argument in node.args:
            values.extend(strings(argument))
    values = sorted({value.strip() for value in values if value.strip() and len(value) > 1})
    catalog: dict[str, str] = {}
    used: set[str] = set()
    for value in values:
        base = slug(value)
        key = base
        suffix = 2
        while key in used:
            key = f"{base}.{suffix}"
            suffix += 1
        used.add(key)
        catalog[key] = value
    UI_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    UI_CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"Wrote {len(catalog)} reviewed UI candidates to {UI_CATALOG}")
    print("Review this catalog before freezing the English source and preparing the queue.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
