from collections.abc import Callable

from playwright.sync_api import Page, expect


def open_questions(
    page: Page,
    load_app: Callable[[Page, str, str], None],
    mode: str,
) -> None:
    load_app(page, "topic-senior-driving.html", f"?mode={mode}")
    page.get_by_role("button", name="Questions／問題").click()


def test_timer_is_hidden_in_participant_mode(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    open_questions(page, load_app, "participant")
    expect(page.locator("#timerRoot")).to_be_hidden()


def test_host_can_choose_start_pause_and_reset_timer(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    open_questions(page, load_app, "host")
    expect(page.locator("#timerRoot")).to_be_visible()
    page.locator("#timerMinutes").select_option("5")
    expect(page.locator("#timerDisplay")).to_have_text("05:00")

    page.locator("#timerStart").click()
    expect(page.locator("#timerDisplay")).not_to_have_text("05:00", timeout=2500)

    page.locator("#timerPause").click()
    paused_value = page.locator("#timerDisplay").text_content()
    page.wait_for_timeout(1200)
    expect(page.locator("#timerDisplay")).to_have_text(paused_value)

    page.locator("#timerReset").click()
    expect(page.locator("#timerDisplay")).to_have_text("05:00")


def test_timer_expiry_shows_silent_visible_alert(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    open_questions(page, load_app, "host")
    page.clock.install()
    page.locator("#timerMinutes").select_option("5")
    page.locator("#timerStart").click()
    page.clock.run_for(5 * 60 * 1000)
    expect(page.locator("#timerStatus")).to_have_text("Time is up／時間到！")
