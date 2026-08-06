from collections.abc import Callable

from playwright.sync_api import Page, expect


def open_questions(page: Page, load_app: Callable[[Page, str, str], None]) -> None:
    load_app(page, "topic-senior-driving.html", "?mode=participant")
    page.get_by_role("button", name="Questions／問題").click()


def test_shows_one_question_and_advances_through_five(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    open_questions(page, load_app)
    expect(page.locator("#questionProgress")).to_have_text("Question 1 of 5")
    expect(page.locator("#questionText")).to_contain_text("renew their licenses")
    page.locator("#nextQuestion").click()
    expect(page.locator("#questionProgress")).to_have_text("Question 2 of 5")
    expect(page.locator("#questionText")).to_contain_text("actual road test")


def test_previous_and_next_stop_at_boundaries(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    open_questions(page, load_app)
    expect(page.locator("#previousQuestion")).to_be_disabled()
    for _ in range(4):
        page.locator("#nextQuestion").click()
    expect(page.locator("#nextQuestion")).to_be_disabled()
    expect(page.locator("#questionProgress")).to_have_text("Question 5 of 5")


def test_show_all_reveals_exactly_five_questions(
    page: Page, load_app: Callable[[Page, str, str], None]
) -> None:
    open_questions(page, load_app)
    page.locator("#toggleAllQuestions").click()
    expect(page.locator("#allQuestions > li")).to_have_count(5)
    expect(page.locator("#allQuestions")).to_be_visible()
