from collections.abc import Callable

import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize(
    ("filename", "search", "heading", "source_pattern", "phrase"),
    [
        (
            "topic-senior-driving.html",
            "?mode=participant",
            "Senior Driver License Renewal in Taiwan",
            r"thb\.gov\.tw",
            "May 31, 2026",
        ),
        (
            "topic-mass-tourism.html",
            "?mode=participant",
            "Mass Tourism in Mallorca",
            r"reuters\.com",
            "July 26, 2026",
        ),
    ],
)
def test_topic_renders_verified_summary_and_source(
    page: Page,
    load_app: Callable[[Page, str, str], None],
    filename: str,
    search: str,
    heading: str,
    source_pattern: str,
    phrase: str,
) -> None:
    load_app(page, filename, search)
    expect(page.get_by_role("heading", name=heading)).to_be_visible()
    expect(page.locator("#articleBody")).to_contain_text(phrase)
    expect(page.locator("#sourceLink")).to_have_attribute("href", re.compile(source_pattern))


def test_topic_page_retains_host_mode_on_home_link(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "topic-senior-driving.html", "?mode=host")
    expect(page.locator("#topicMode")).to_have_value("host")
    expect(page.locator("#homeLink")).to_have_attribute("href", "index.html?mode=host")


def test_mass_tourism_includes_a_full_background_article_link(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "topic-mass-tourism.html", "?mode=participant")
    expect(page.locator("#backgroundSourceLink")).to_be_visible()
    expect(page.locator("#backgroundSourceLink")).to_have_attribute(
        "href",
        "https://www.reuters.com/world/europe/thousands-protest-spains-mallorca-against-mass-tourism-2024-07-21/",
    )
