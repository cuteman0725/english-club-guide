from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path
from zipfile import ZipFile

from playwright.sync_api import Page, expect

ROOT = Path(__file__).resolve().parents[1]


def test_static_site_verifier_accepts_local_runtime_assets() -> None:
    result = subprocess.run(
        ["python", "scripts/verify_static_site.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Static-site verification passed" in result.stdout


def test_primary_interactions_need_no_remote_runtime_assets(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "topic-mass-tourism.html", "?mode=host")
    expect(page.locator("#topicTitle")).to_have_text("Mass Tourism in Mallorca")
    page.get_by_role("button", name="Visual Summary／圖解").click()
    expect(page.locator("#visualImage")).to_have_attribute(
        "src", "images/mass-tourism-article-summary.png"
    )
    page.get_by_role("button", name="Questions／問題").click()
    expect(page.locator("#questionProgress")).to_have_text("Question 1 of 5")
    expect(page.locator("#timerRoot")).to_be_visible()


def test_offline_zip_contains_deployable_site_at_archive_root() -> None:
    result = subprocess.run(
        ["python", "scripts/make_offline_zip.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    zip_path = ROOT / "dist/english-club-guide-offline.zip"
    assert zip_path.is_file()
    with ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "index.html" in names
    assert "topic-senior-driving.html" in names
    assert "topic-mass-tourism.html" in names
    assert "images/senior-driving-summary.png" in names
    assert "images/mass-tourism-article-summary.png" in names
    assert "images/mass-tourism-questions.png" in names
    assert not any(name.startswith("english-club-guide/") for name in names)
