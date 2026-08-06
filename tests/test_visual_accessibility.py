from collections.abc import Callable
from pathlib import Path
import re

from playwright.sync_api import Page, expect

ROOT = Path(__file__).resolve().parents[1]


def test_required_infographic_files_exist() -> None:
    assert (ROOT / "images/senior-driving-summary.png").is_file()
    assert (ROOT / "images/mass-tourism-article-summary.png").is_file()
    assert (ROOT / "images/mass-tourism-questions.png").is_file()


def test_topic_image_has_meaningful_alt_text_and_disclosure(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "topic-mass-tourism.html", "?mode=participant")
    page.get_by_role("button", name="Visual Summary／圖解").click()
    expect(page.locator("#visualImage")).to_have_attribute("alt", re.compile("Mallorca", re.I))
    expect(page.locator("#visualDisclosure")).to_contain_text("AI-generated")
    expect(page.locator("#visualDisclosure")).to_contain_text(
        "not original Reuters photographs"
    )


def test_image_can_be_enlarged_and_closed_with_focus_restored(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "topic-senior-driving.html", "?mode=participant")
    page.get_by_role("button", name="Visual Summary／圖解").click()
    page.locator("#visualOpenButton").click()
    expect(page.locator("#imageDialog")).to_have_js_property("open", True)
    page.get_by_role("button", name="Close enlarged image").click()
    expect(page.locator("#visualOpenButton")).to_be_focused()


def test_first_interactive_control_is_home_link(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "topic-senior-driving.html", "?mode=host")
    page.keyboard.press("Tab")
    expect(page.locator("#homeLink")).to_be_focused()
