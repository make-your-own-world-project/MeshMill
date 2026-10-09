"""Serve MeshMill's local, single-batch browser translation queue."""

from __future__ import annotations

import datetime as dt
import html
import json
import math
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from config import PORT, WORK

QUEUE_PATH = WORK / "queue.json"
CACHE_PATH = WORK / "translation-cache.json"
PROGRESS_PATH = WORK / "progress.json"
RESULTS = WORK / "batch-results"
MARKER_RE = re.compile(r"\[\[(\d{8})\]\]\s*(.*?)(?=\[\[\d{8}\]\]|\Z)", re.DOTALL)

queue = json.loads(QUEUE_PATH.read_text("utf-8"))
cache = json.loads(CACHE_PATH.read_text("utf-8"))
persisted = json.loads(PROGRESS_PATH.read_text("utf-8")) if PROGRESS_PATH.exists() else {}
state = {
    "saved_batches": int(persisted.get("saved_batches", 0)),
    "last_saved": persisted.get("last_saved"),
    "validation_error": str(persisted.get("validation_error", "")),
}


def save_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", "utf-8")
    temporary.replace(path)


def pending_batch() -> list[dict[str, object]]:
    batch: list[dict[str, object]] = []
    size = 0
    locale: str | None = None
    for index, row in enumerate(queue):
        if row["key"] in cache:
            continue
        if locale is not None and row["locale"] != locale:
            break
        segment = f'[[{10000000 + index}]]\n{row["protected_source"]}'
        if batch and size + len(segment) + 2 > 3800:
            break
        locale = str(row["locale"])
        size += len(segment) + 2
        batch.append({"marker": 10000000 + index, **row})
    return batch


def update_progress(status: str = "translating") -> None:
    existing = json.loads(PROGRESS_PATH.read_text("utf-8")) if PROGRESS_PATH.exists() else {}
    existing.update(
        {
            "status": status,
            "translation_started": state["saved_batches"] > 0 or existing.get("translation_started", False),
            "saved_batches": state["saved_batches"],
            "last_saved": state["last_saved"],
            "validation_error": state["validation_error"],
            "remaining_passages": sum(row["key"] not in cache for row in queue),
            "updated_at": dt.datetime.now(dt.UTC).isoformat(),
        }
    )
    save_json_atomic(PROGRESS_PATH, existing)


def dashboard_html() -> bytes:
    live_progress = json.loads(PROGRESS_PATH.read_text("utf-8")) if PROGRESS_PATH.exists() else {}
    total = len(queue)
    remaining = sum(row["key"] not in cache for row in queue)
    completed = total - remaining
    percent = (completed / total * 100.0) if total else 100.0
    current = next((str(row["locale"]) for row in queue if row["key"] not in cache), "complete")
    per_language: dict[str, list[int]] = {}
    for row in queue:
        counts = per_language.setdefault(str(row["locale"]), [0, 0])
        counts[0] += 1
        counts[1] += int(row["key"] in cache)
    remaining_batches = 0
    for locale, (language_total, language_done) in per_language.items():
        pending = language_total - language_done
        if pending:
            language_rows = [row for row in queue if row["locale"] == locale and row["key"] not in cache]
            size = 0
            batches = 0
            for row in language_rows:
                segment_size = len(str(row["protected_source"])) + 15
                if size and size + segment_size > 3800:
                    batches += 1
                    size = 0
                size += segment_size
            remaining_batches += batches + int(size > 0)
    current_batch = pending_batch()
    current_batch_label = (
        f'{current_batch[0]["marker"]}-{current_batch[-1]["marker"]} '
        f'({len(current_batch)} passages)'
        if current_batch else "None"
    )
    current_total, current_done = per_language.get(current, [0, 0])
    current_percent = (current_done / current_total * 100.0) if current_total else 100.0
    recent_results = sorted(RESULTS.glob("*.json"), key=lambda path: path.stat().st_mtime)[-20:]
    recent_passages = 0
    elapsed_seconds = 0.0
    if len(recent_results) >= 2:
        recent_passages = sum(
            len(json.loads(path.read_text("utf-8")).get("batch", []))
            for path in recent_results[1:]
        )
        elapsed_seconds = recent_results[-1].stat().st_mtime - recent_results[0].stat().st_mtime
    passages_per_minute = recent_passages / elapsed_seconds * 60.0 if elapsed_seconds > 0 else 0.0
    eta_seconds = remaining / (passages_per_minute / 60.0) if passages_per_minute > 0 else 0.0
    if not remaining:
        eta = "Complete"
    elif not eta_seconds:
        eta = "Calculating"
    else:
        eta_minutes = max(1, math.ceil(eta_seconds / 60.0))
        hours, minutes = divmod(eta_minutes, 60)
        eta = f"{hours} hr {minutes} min" if hours else f"{minutes} min"
    rows = "".join(
        f"<tr><td>{html.escape(locale)}</td><td>{done:,}</td><td>{language_total:,}</td>"
        f"<td>{(done / language_total * 100.0 if language_total else 100.0):.1f}%</td>"
        f"<td>{language_total - done:,}</td></tr>"
        for locale, (language_total, done) in per_language.items()
    )
    error = html.escape(state["validation_error"] or "None")
    return f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="10">
<title>MeshMill translation progress</title>
<style>body{{font:16px system-ui;margin:24px;max-width:1000px;color:#17233a}}a{{color:#2563ff}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
.card{{border:1px solid #d8dee9;border-radius:8px;padding:12px}}.value{{font-size:1.5rem;font-weight:650}}
progress{{width:100%;height:22px}}table{{border-collapse:collapse;width:100%;margin-top:18px}}
th,td{{padding:8px;border-bottom:1px solid #d8dee9;text-align:right}}th:first-child,td:first-child{{text-align:left}}
.error{{color:#a00}}</style><body><p><a href="/">Batch interface</a></p>
<h1>Translation progress</h1><progress value="{completed}" max="{total}"></progress>
<div class="cards"><div class="card">Completed<div class="value">{completed:,}</div></div>
<div class="card">Remaining<div class="value">{remaining:,}</div></div>
<div class="card">Progress<div class="value">{percent:.2f}%</div></div>
<div class="card">Current language<div class="value">{html.escape(current)}</div></div>
<div class="card">Language progress<div class="value">{current_done:,}/{current_total:,}</div><div>{current_percent:.1f}%</div></div>
<div class="card">Saved batches<div class="value">{state['saved_batches']:,}</div></div>
<div class="card">Estimated batches left<div class="value">{remaining_batches:,}</div></div>
<div class="card">Recent rate<div class="value">{passages_per_minute:.1f}/min</div></div>
<div class="card">Estimated time left<div class="value">{eta}</div></div></div>
<dl><dt>Last successful batch</dt><dd>{html.escape(str(state['last_saved'] or 'None'))}</dd>
<dt>Current batch</dt><dd>{html.escape(current_batch_label)}</dd>
<dt>Last update</dt><dd>{html.escape(str(live_progress.get('updated_at', 'Unknown')))}</dd>
<dt>Errors</dt><dd class="error">{error}</dd></dl>
<table><thead><tr><th>Language</th><th>Completed</th><th>Total</th><th>Progress</th><th>Remaining</th></tr></thead>
<tbody>{rows}</tbody></table></body></html>""".encode()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_: object) -> None:
        return

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/dashboard":
            body = dashboard_html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        if path != "/":
            self.send_error(404)
            return
        batch = pending_batch()
        locale = str(batch[0]["locale"]) if batch else "complete"
        source = "\n\n".join(
            f'[[{row["marker"]}]]\n{row["protected_source"]}' for row in batch
        )
        remaining = sum(row["key"] not in cache for row in queue)
        body = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><title>MeshMill translation queue</title>
<style>body{{font:16px system-ui;margin:24px;max-width:1000px}}textarea{{width:100%;box-sizing:border-box}}
.error{{color:#a00}}dl{{display:grid;grid-template-columns:max-content 1fr;gap:4px 16px}}</style>
<body><h1>MeshMill translation queue</h1><dl>
<dt>Language</dt><dd id="locale">{html.escape(locale)}</dd>
<dt>Remaining passages</dt><dd>{remaining}</dd>
<dt>Saved batches</dt><dd>{state['saved_batches']}</dd>
<dt>Last saved markers</dt><dd>{html.escape(str(state['last_saved'] or 'None'))}</dd>
</dl><p class="error">{html.escape(state['validation_error'])}</p>
<label for="source">Source batch</label>
<textarea id="source" readonly rows="15">{html.escape(source)}</textarea>
<form method="post"><input type="hidden" name="locale" value="{html.escape(locale)}">
<label for="result">Translated result</label>
<textarea id="result" name="result" rows="15" autofocus></textarea>
<button type="submit">Save verified batch</button></form></body></html>""".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        batch = pending_batch()
        length = int(self.headers.get("Content-Length", "0"))
        if length > 200_000:
            self.send_error(413)
            return
        form = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
        result = form.get("result", [""])[0]
        submitted_locale = form.get("locale", [""])[0]
        try:
            if not batch:
                raise ValueError("The queue is already complete")
            expected_locale = str(batch[0]["locale"])
            if submitted_locale != expected_locale:
                raise ValueError("Destination language does not match the current batch")
            chunks = MARKER_RE.findall(result)
            expected = [int(row["marker"]) for row in batch]
            actual = [int(marker) for marker, _ in chunks]
            if actual != expected:
                raise ValueError("Missing, duplicate, additional, or reordered markers")
            if not all(text.strip() and "\ufffd" not in text for _, text in chunks):
                raise ValueError("A translated passage is empty or contains invalid text")
            for row, (_, translated) in zip(batch, chunks):
                cache[str(row["key"])] = translated.strip()
            save_json_atomic(CACHE_PATH, cache)
            RESULTS.mkdir(parents=True, exist_ok=True)
            first, last = expected[0], expected[-1]
            save_json_atomic(
                RESULTS / f"{first}-{last}.json",
                {"locale": expected_locale, "batch": batch, "translated_result": result},
            )
            state["saved_batches"] += 1
            state["last_saved"] = f"{first}-{last}"
            state["validation_error"] = ""
            update_progress("complete" if not pending_batch() else "translating")
        except Exception as error:  # noqa: BLE001 - validation failures are displayed in the local UI
            state["validation_error"] = str(error)
            update_progress("translation_error")
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


if __name__ == "__main__":
    RESULTS.mkdir(parents=True, exist_ok=True)
    update_progress("ready")
    print(f"MeshMill translation queue ready at http://127.0.0.1:{PORT}", flush=True)
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
