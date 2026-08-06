from collections.abc import Callable

from playwright.sync_api import Page, expect


def test_home_displays_two_topic_choices(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "index.html", "")
    expect(page.get_by_role("heading", name="Choose a discussion topic")).to_be_visible()
    expect(page.locator("#topicSeniorDriving")).to_contain_text("Senior Driver")
    expect(page.locator("#topicMassTourism")).to_contain_text("Mass Tourism")


def test_selected_mode_is_carried_into_both_topic_urls(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "index.html", "")
    page.locator("#homeMode").select_option("host")
    expect(page.locator("#topicSeniorDriving")).to_have_attribute(
        "href", "topic-senior-driving.html?mode=host"
    )
    expect(page.locator("#topicMassTourism")).to_have_attribute(
        "href", "topic-mass-tourism.html?mode=host"
    )


def test_unknown_mode_falls_back_to_participant(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "index.html", "?mode=unknown")
    expect(page.locator("#homeMode")).to_have_value("participant")
