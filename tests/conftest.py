from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Callable

import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    browser = playwright_instance.chromium.launch(
        headless=True,
        executable_path="/usr/bin/chromium",
        args=["--no-sandbox"],
    )
    yield browser
    browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.set_default_timeout(3000)
    yield page
    context.close()


@pytest.fixture
def load_app() -> Callable[[Page, str, str], None]:
    def load(page: Page, filename: str, search: str = "") -> None:
        source_path = ROOT / filename
        source = source_path.read_text(encoding="utf-8")

        def inline_style(match: re.Match[str]) -> str:
            path = ROOT / match.group(1)
            return f"<style>\n{path.read_text(encoding='utf-8')}\n</style>"

        source = re.sub(
            r'<link\s+rel="stylesheet"\s+href="([^"]+)"(?:\s+media="([^"]+)")?\s*>',
            lambda match: (
                f'<style media="{match.group(2)}">\n'
                f'{(ROOT / match.group(1)).read_text(encoding="utf-8")}\n</style>'
                if match.group(2)
                else inline_style(match)
            ),
            source,
        )

        def inline_script(match: re.Match[str]) -> str:
            path = ROOT / match.group(1)
            return f"<script>\n{path.read_text(encoding='utf-8')}\n</script>"

        source = re.sub(
            r'<script\s+defer\s+src="([^"]+)"\s*></script>',
            inline_script,
            source,
        )

        escaped_search = search.replace("\\", "\\\\").replace("'", "\\'")
        search_shim = f"""
<script>
(() => {{
  const NativeURLSearchParams = window.URLSearchParams;
  const desiredSearch = '{escaped_search}';
  window.URLSearchParams = function(input) {{
    return new NativeURLSearchParams(input === '' ? desiredSearch : input);
  }};
  window.URLSearchParams.prototype = NativeURLSearchParams.prototype;
}})();
</script>
"""
        source = source.replace("<head>", "<head>" + search_shim, 1)
        page.set_content(source, wait_until="load")

    return load
