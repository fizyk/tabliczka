"""Tests for the question page."""

from collections.abc import Iterator

import pytest
from PySide6.QtCore import QLocale, Qt
from pytestqt.qtbot import QtBot

from tabliczka.practice.api import Drill
from tabliczka.practice.models import Score
from tabliczka.ui.gui.pages.question import QuestionPage


@pytest.fixture
def english_locale() -> Iterator[None]:
    """Use a locale whose group separator is a comma."""
    default = QLocale()
    QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
    yield
    QLocale.setDefault(default)


@pytest.mark.parametrize(("typed", "correct"), [("2", True), ("4", False)])
def test_question_page__answered(
    qtbot: QtBot, addition_only: None, typed: str, *, correct: bool
) -> None:
    """Each scored answer is reported with its question and whether it was correct."""
    # Given
    page = QuestionPage("Ala", Drill(["add"]))
    qtbot.addWidget(page)
    question = page.question
    qtbot.keyClicks(page.given, typed)

    # When
    with qtbot.waitSignal(page.answered) as answered:
        qtbot.keyClick(page.given, Qt.Key.Key_Return)

    # Then
    assert answered.args == [question, correct]
    assert page.given.text() == ""


@pytest.mark.parametrize("typed", ["", "-", "dwa", "1,000"])
def test_question_page__ignores(
    qtbot: QtBot, addition_only: None, english_locale: None, typed: str
) -> None:
    """Enter does nothing until a whole number is typed."""
    # Given
    page = QuestionPage("Ala", Drill(["add"]))
    qtbot.addWidget(page)
    page.given.setText(typed)

    # When / Then
    with qtbot.assertNotEmitted(page.answered):
        qtbot.keyClick(page.given, Qt.Key.Key_Return)
    assert page.drill.summary().total == Score()


def test_question_page__finished(qtbot: QtBot, addition_only: None) -> None:
    """The page finishes after the drill's last question."""
    # Given
    page = QuestionPage("Ala", Drill(["add"], question_count=1))
    qtbot.addWidget(page)
    qtbot.keyClicks(page.given, "2")

    # When / Then
    with qtbot.waitSignal(page.finished):
        qtbot.keyClick(page.given, Qt.Key.Key_Return)
