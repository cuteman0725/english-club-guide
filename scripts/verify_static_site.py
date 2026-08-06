from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "topic-senior-driving.html",
    ROOT / "topic-mass-tourism.html",
]
REQUIRED_ASSETS = [
    ROOT / "images/senior-driving-summary.png",
    ROOT / "images/mass-tourism-article-summary.png",
    ROOT / "images/mass-tourism-questions.png",
]

errors: list[str] = []

for path in [*HTML_FILES, *REQUIRED_ASSETS]:
    if not path.exists():
        errors.append(f"Missing required file: {path.relative_to(ROOT)}")

remote_runtime_patterns = [
    re.compile(r'<script[^>]+src=["\']https?://', re.I),
    re.compile(r'<link[^>]+href=["\']https?://', re.I),
    re.compile(r'<img[^>]+src=["\']https?://', re.I),
    re.compile(r'@import\s+(?:url\()?\s*["\']?https?://', re.I),
    re.compile(r'url\(\s*["\']?https?://', re.I),
]
local_asset_pattern = re.compile(
    r'(?:src|href)=["\'](?!#|mailto:|tel:|https?://)([^"\'?]+)(?:\?[^"\']*)?["\']',
    re.I,
)

for html_path in HTML_FILES:
    if not html_path.exists():
        continue
    source = html_path.read_text(encoding="utf-8")
    for pattern in remote_runtime_patterns:
        if pattern.search(source):
            errors.append(
                f"{html_path.relative_to(ROOT)} contains a remote runtime dependency"
            )
    for match in local_asset_pattern.finditer(source):
        target = (html_path.parent / match.group(1)).resolve()
        if not target.exists():
            errors.append(
                f"{html_path.relative_to(ROOT)} references missing local asset "
                f"{match.group(1)}"
            )

for path in sorted((ROOT / "js").glob("*.js")):
    source = path.read_text(encoding="utf-8")
    forbidden = {
        "fetch(": "fetch is forbidden for the offline runtime",
        "localStorage": "localStorage is out of scope",
        "sessionStorage": "sessionStorage is out of scope",
        "serviceWorker.register": "service workers are out of scope",
    }
    for needle, message in forbidden.items():
        if needle in source:
            errors.append(f"{path.relative_to(ROOT)}: {message}")

for path in sorted((ROOT / "css").glob("*.css")):
    source = path.read_text(encoding="utf-8")
    for pattern in remote_runtime_patterns[3:]:
        if pattern.search(source):
            errors.append(f"{path.relative_to(ROOT)} contains a remote CSS dependency")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print("Static-site verification passed.")
