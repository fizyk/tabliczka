"""Tests for the window."""

import sys
from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QLocale, Qt
from PySide6.QtWidgets import QApplication, QMessageBox
from pytestqt.qtbot import QtBot

from tabliczka.exercises.service import ADD
from tabliczka.practice.models import Score, Summary
from tabliczka.ui.window import (
    DrillWindow,
    QuestionPage,
    StartPage,
    SummaryPage,
    main,
    show_error,
    summary_html,
)


@pytest.fixture
def english_locale() -> Iterator[None]:
    """Use a locale whose group separator is a comma."""
    default = QLocale()
    QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
    yield
    QLocale.setDefault(default)


@pytest.fixture
def addition_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make every question ``1+1``."""
    monkeypatch.setattr("tabliczka.practice.service.choice", lambda operations: ADD)
    monkeypatch.setattr("tabliczka.exercises.service.randint", lambda low, high: low)


def choose(page: StartPage, name: str, operation_ids: list[str]) -> None:
    """Type the name and choose only the operations with the given ids."""
    page.name.setText(name)
    for operation_id, box in page.operation_boxes.items():
        box.setChecked(operation_id in operation_ids)


@pytest.mark.parametrize(
    ("name", "operation_ids", "enabled"),
    [
        ("Ala", ["add"], True),
        ("  ", ["add"], False),
        ("Ala", [], False),
    ],
)
def test_start_page__start_button(
    qtbot: QtBot, name: str, operation_ids: list[str], *, enabled: bool
) -> None:
    """The drill starts only with a name and at least one operation."""
    # Given
    page = StartPage()
    qtbot.addWidget(page)

    # When
    choose(page, name, operation_ids)

    # Then
    assert page.start_button.isEnabled() is enabled


@pytest.mark.parametrize(
    ("operation_ids", "minimum"),
    [(["add", "subtract"], 1), (["multiplication", "division"], 0), ([], 0)],
)
def test_start_page__largest_number_default(
    qtbot: QtBot, operation_ids: list[str], minimum: int
) -> None:
    """The largest number stays each operation's own until chosen."""
    # Given
    page = StartPage()
    qtbot.addWidget(page)

    # When
    choose(page, "Ala", operation_ids)

    # Then
    assert page.max_n.minimum() == minimum
    assert page.max_n.text() == "domyślna"
    assert page.chosen_max_n() is None


@pytest.mark.parametrize(("chosen", "max_n"), [(1, 2), (5, 5)])
def test_start_page__largest_number_chosen(
    qtbot: QtBot, chosen: int, max_n: int
) -> None:
    """A chosen largest number stays chosen, raised to what the operations allow."""
    # Given
    page = StartPage()
    qtbot.addWidget(page)
    choose(page, "Ala", ["multiplication"])
    page.max_n.setValue(chosen)

    # When
    page.operation_boxes["add"].setChecked(True)

    # Then
    assert page.chosen_max_n() == max_n


def test_start_page__chosen_values(qtbot: QtBot) -> None:
    """The chosen largest number and number of questions are passed on."""
    # Given
    page = StartPage()
    qtbot.addWidget(page)

    # When
    choose(page, " Ala ", ["division", "add"])
    page.max_n.setValue(12)
    page.question_count.setValue(5)

    # Then
    assert page.learner_name() == "Ala"
    assert page.operation_ids() == ["add", "division"]
    assert page.chosen_max_n() == 12
    assert page.chosen_question_count() == 5


def test_drill_window(qtbot: QtBot, addition_only: None) -> None:
    """The learner answers each question, sees the feedback, then the summary."""
    # Given
    window = DrillWindow()
    qtbot.addWidget(window)
    choose(window.start_page, "Ala", ["add"])
    window.start_page.question_count.setValue(2)
    qtbot.mouseClick(window.start_page.start_button, Qt.MouseButton.LeftButton)
    page = window.pages.currentWidget()
    assert isinstance(page, QuestionPage)

    # When / Then
    assert page.question_label.text() == "Dodawanie: Ile to 1+1?"
    qtbot.keyClicks(page.answer, "2")
    qtbot.keyClick(page.answer, Qt.Key.Key_Return)
    assert "Dobrze!" in window.feedback.text()
    qtbot.keyClicks(page.answer, "4")
    qtbot.keyClick(page.answer, Qt.Key.Key_Return)
    assert "Niestety, źle, prawidłowy wynik to 2." in window.feedback.text()
    summary = window.pages.currentWidget()
    assert isinstance(summary, SummaryPage)
    assert "1 - dobrze" in summary.text()
    assert "1 - źle" in summary.text()


def test_drill_window__stop(qtbot: QtBot, addition_only: None) -> None:
    """The stop button shows the summary of the answers so far."""
    # Given
    window = DrillWindow()
    qtbot.addWidget(window)
    choose(window.start_page, "Ala", ["add"])
    qtbot.mouseClick(window.start_page.start_button, Qt.MouseButton.LeftButton)
    page = window.pages.currentWidget()
    assert isinstance(page, QuestionPage)
    qtbot.keyClicks(page.answer, "2")
    qtbot.keyClick(page.answer, Qt.Key.Key_Return)

    # When
    qtbot.mouseClick(page.stop_button, Qt.MouseButton.LeftButton)

    # Then
    summary = window.pages.currentWidget()
    assert isinstance(summary, SummaryPage)
    assert "1 - dobrze" in summary.text()


@pytest.mark.parametrize("typed", ["", "-", "dwa", "1,000"])
def test_question_page__ignores(
    qtbot: QtBot, addition_only: None, english_locale: None, typed: str
) -> None:
    """Enter does nothing until a whole number is typed."""
    # Given
    window = DrillWindow()
    qtbot.addWidget(window)
    choose(window.start_page, "Ala", ["add"])
    qtbot.mouseClick(window.start_page.start_button, Qt.MouseButton.LeftButton)
    page = window.pages.currentWidget()
    assert isinstance(page, QuestionPage)
    page.answer.setText(typed)

    # When
    qtbot.keyClick(page.answer, Qt.Key.Key_Return)

    # Then
    assert window.feedback.text() == ""
    assert page.drill.summary().total == Score()


def test_summary_html() -> None:
    """The summary shows the totals, then each operation's own score."""
    # Given
    summary = Summary(
        total=Score(correct=2, wrong=1),
        scores={"add": Score(correct=2), "subtract": Score(wrong=1)},
    )

    # When
    html = summary_html(summary)

    # Then
    assert html == (
        'Twój wynik to:<br><span style="color: green">2 - dobrze</span>'
        '<br><span style="color: red">1 - źle</span>'
        '<hr>Dodawanie:<br><span style="color: green">2 - dobrze</span>'
        '<hr>Odejmowanie:<br><span style="color: green">0 - dobrze</span>'
        '<br><span style="color: red">1 - źle</span>'
    )


def test_show_error(monkeypatch: pytest.MonkeyPatch, qapp: QApplication) -> None:
    """An unexpected error is shown in a message, with its traceback in the details."""
    # Given
    shown: list[QMessageBox] = []
    monkeypatch.setattr(QMessageBox, "exec", lambda message: shown.append(message))
    error = RuntimeError("boom")

    # When
    show_error(RuntimeError, error, None)

    # Then
    [message] = shown
    assert message.text() == (
        "Coś poszło nie tak. Zamknij program i uruchom go jeszcze raz."
    )
    assert "RuntimeError: boom" in message.detailedText()


def test_main(monkeypatch: pytest.MonkeyPatch, qapp: QApplication) -> None:
    """The window opens and unexpected errors are shown until it closes."""
    # Given
    application_mock = MagicMock(spec=QApplication)
    application_mock.return_value.exec.return_value = 0
    monkeypatch.setattr("tabliczka.ui.window.QApplication", application_mock)
    monkeypatch.setattr(sys, "excepthook", sys.excepthook)

    # When
    with pytest.raises(SystemExit) as exit_info:
        main()

    # Then
    assert exit_info.value.code == 0
    assert sys.excepthook is show_error
