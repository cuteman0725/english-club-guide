from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT = DIST / "english-club-guide-offline.zip"

included = [
    ROOT / "index.html",
    ROOT / "topic-senior-driving.html",
    ROOT / "topic-mass-tourism.html",
    ROOT / "README.md",
    *sorted((ROOT / "css").glob("*.css")),
    *sorted((ROOT / "js").glob("*.js")),
    *sorted((ROOT / "images").glob("*.png")),
]

missing = [path for path in included if not path.exists()]
if missing:
    raise SystemExit("Missing package files:\n" + "\n".join(map(str, missing)))

DIST.mkdir(exist_ok=True)
with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for source in included:
        relative = source.relative_to(ROOT).as_posix()
        info = ZipInfo(relative, date_time=(2026, 8, 6, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, source.read_bytes())

print(OUTPUT)
