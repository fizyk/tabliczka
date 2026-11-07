"""Tests for the window that moves between the pages."""

from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tabliczka.ui.gui.drill_window import DrillWindow
from tabliczka.ui.gui.pages.question import QuestionPage
from tabliczka.ui.gui.pages.summary import SummaryPage


def test_drill_window(qtbot: QtBot, addition_only: None) -> None:
    """The learner answers each question, sees the feedback, then the summary."""
    # Given
    window = DrillWindow()
    qtbot.addWidget(window)
    window.start_page.name.setText("Ala")
    window.start_page.question_count.setValue(2)
    qtbot.mouseClick(window.start_page.start_button, Qt.MouseButton.LeftButton)
    page = window.pages.currentWidget()
    assert isinstance(page, QuestionPage)

    # When / Then
    assert page.question_label.text() == "Dodawanie: Ile to 1+1?"
    qtbot.keyClicks(page.given, "2")
    qtbot.keyClick(page.given, Qt.Key.Key_Return)
    assert "Dobrze!" in window.feedback.text()
    qtbot.keyClicks(page.given, "4")
    qtbot.keyClick(page.given, Qt.Key.Key_Return)
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
    window.start_page.name.setText("Ala")
    qtbot.mouseClick(window.start_page.start_button, Qt.MouseButton.LeftButton)
    page = window.pages.currentWidget()
    assert isinstance(page, QuestionPage)
    qtbot.keyClicks(page.given, "2")
    qtbot.keyClick(page.given, Qt.Key.Key_Return)

    # When
    qtbot.mouseClick(page.stop_button, Qt.MouseButton.LeftButton)

    # Then
    summary = window.pages.currentWidget()
    assert isinstance(summary, SummaryPage)
    assert "1 - dobrze" in summary.text()
