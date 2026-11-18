"""Tests for the question page."""

from collections.abc import Iterator

import pytest
from PySide6.QtCore import QLocale, Qt
from pytestqt.qtbot import QtBot

from tabliczka.exercises.service import DIVIDE_WITH_REMAINDER
from tabliczka.practice import Drill
from tabliczka.practice.models import Score
from tabliczka.ui.gui.pages.question import QuestionPage


@pytest.fixture
def english_locale() -> Iterator[None]:
    """Use a locale whose group separator is a comma."""
    default = QLocale()
    QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
    yield
    QLocale.setDefault(default)


@pytest.fixture
def division_with_remainder_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make every question ``3:2``, answered 1 with a remainder of 1."""
    monkeypatch.setattr(
        "tabliczka.practice.service.choice", lambda operations: DIVIDE_WITH_REMAINDER
    )
    monkeypatch.setattr("tabliczka.exercises.service.randint", lambda low, high: low)


@pytest.mark.parametrize(("typed", "correct"), [("2", True), ("4", False)])
def test_question_page__answered(
    qtbot: QtBot, addition_only: None, typed: str, *, correct: bool
) -> None:
    """Each scored answer is reported with its question and whether it was correct."""
    # Given
    page = QuestionPage("Ala", Drill(["add"]))
    qtbot.addWidget(page)
    question = page.question
    qtbot.keyClicks(page.given_answer, typed)

    # When
    with qtbot.waitSignal(page.answered) as answered:
        qtbot.keyClick(page.given_answer, Qt.Key.Key_Return)

    # Then
    assert answered.args == [question, correct]
    assert page.given_answer.text() == ""


@pytest.mark.parametrize("typed", ["", "-", "dwa", "1,000"])
def test_question_page__ignores(
    qtbot: QtBot, addition_only: None, english_locale: None, typed: str
) -> None:
    """Enter does nothing until a whole number is typed."""
    # Given
    page = QuestionPage("Ala", Drill(["add"]))
    qtbot.addWidget(page)
    page.given_answer.setText(typed)

    # When / Then
    with qtbot.assertNotEmitted(page.answered):
        qtbot.keyClick(page.given_answer, Qt.Key.Key_Return)
    assert page.drill.summary().total == Score()


def test_question_page__finished(qtbot: QtBot, addition_only: None) -> None:
    """The page finishes after the drill's last question."""
    # Given
    page = QuestionPage("Ala", Drill(["add"], question_count=1))
    qtbot.addWidget(page)
    qtbot.keyClicks(page.given_answer, "2")

    # When / Then
    with qtbot.waitSignal(page.finished):
        qtbot.keyClick(page.given_answer, Qt.Key.Key_Return)


def test_question_page__no_remainder_field(qtbot: QtBot, addition_only: None) -> None:
    """A question answered with one number shows no remainder field."""
    # When
    page = QuestionPage("Ala", Drill(["add"]))
    qtbot.addWidget(page)

    # Then
    assert page.given_remainder.isHidden()
    assert page.remainder_label.isHidden()


@pytest.mark.parametrize(("typed_remainder", "correct"), [("1", True), ("0", False)])
def test_question_page__answered_with_remainder(
    qtbot: QtBot,
    division_with_remainder_only: None,
    typed_remainder: str,
    *,
    correct: bool,
) -> None:
    """A division with remainder is scored once both fields hold a whole number."""
    # Given
    page = QuestionPage("Ala", Drill(["division_with_remainder"]))
    qtbot.addWidget(page)
    question = page.question
    page.given_answer.setText("1")
    page.given_remainder.setText(typed_remainder)

    # When
    with qtbot.waitSignal(page.answered) as answered:
        qtbot.keyClick(page.given_remainder, Qt.Key.Key_Return)

    # Then
    assert not page.given_remainder.isHidden()
    assert answered.args == [question, correct]
    assert (page.given_answer.text(), page.given_remainder.text()) == ("", "")


def test_question_page__waits_for_remainder(
    qtbot: QtBot, division_with_remainder_only: None
) -> None:
    """Enter after the quotient alone does not score the answer."""
    # Given
    page = QuestionPage("Ala", Drill(["division_with_remainder"]))
    qtbot.addWidget(page)
    page.given_answer.setText("1")

    # When / Then
    with qtbot.assertNotEmitted(page.answered):
        qtbot.keyClick(page.given_answer, Qt.Key.Key_Return)
    assert page.drill.summary().total == Score()
