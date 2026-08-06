from collections.abc import Callable

from playwright.sync_api import Page, expect


def test_320px_layout_has_no_horizontal_overflow(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    page.set_viewport_size({"width": 320, "height": 700})
    load_app(page, "topic-mass-tourism.html", "?mode=host")
    sizes = page.evaluate(
        "({scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth})"
    )
    assert sizes["scrollWidth"] <= sizes["clientWidth"]


def test_print_mode_shows_all_content_and_hides_controls(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    load_app(page, "topic-senior-driving.html", "?mode=host")
    page.emulate_media(media="print")

    expect(page.locator("#articlePanel")).to_be_visible()
    expect(page.locator("#visualPanel")).to_be_visible()
    expect(page.locator("#questionsPanel")).to_be_visible()
    expect(page.locator("#allQuestions")).to_be_visible()
    expect(page.locator("#topicMode")).to_be_hidden()
    expect(page.locator("#timerRoot")).to_be_hidden()
    expect(page.locator(".tab-list")).to_be_hidden()


def test_routine_text_is_at_least_16px_on_mobile(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    page.set_viewport_size({"width": 320, "height": 700})
    load_app(page, "topic-senior-driving.html", "?mode=participant")
    font_size = page.locator("#articleBody p").first.evaluate(
        "element => Number.parseFloat(getComputedStyle(element).fontSize)"
    )
    assert font_size >= 16


def test_print_remains_white_and_readable_when_device_prefers_dark_mode(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    page.emulate_media(media="print", color_scheme="dark")
    load_app(page, "topic-senior-driving.html", "?mode=participant")
    colors = page.locator("#articlePanel").evaluate(
        "element => ({background: getComputedStyle(element).backgroundColor, color: getComputedStyle(element).color})"
    )
    assert colors["background"] == "rgb(255, 255, 255)"
    assert colors["color"] == "rgb(0, 0, 0)"
