"""Tests for the window that moves between the pages."""

from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tabliczka.profiles import load_profile, save_profile
from tabliczka.profiles.models import Profile
from tabliczka.releases.models import Release
from tabliczka.ui.gui.drill_window import DrillWindow
from tabliczka.ui.gui.pages.question import QuestionPage
from tabliczka.ui.gui.pages.summary import SummaryPage


def test_drill_window(qtbot: QtBot, addition_only: None) -> None:
    """The learner answers each question, sees the feedback, then the summary."""
    # Given
    window = DrillWindow()
    qtbot.addWidget(window)
    window.start_page.name.setText("Ala")
    window.start_page.operation_boxes["add"].setChecked(True)
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
    window.start_page.operation_boxes["add"].setChecked(True)
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


def test_drill_window__saved_profile(qtbot: QtBot, addition_only: None) -> None:
    """The start page shows the saved profile, and starting saves the changes."""
    # Given
    save_profile(Profile("Ala", ("add",), largest_number=12, question_count=5))
    window = DrillWindow()
    qtbot.addWidget(window)
    assert window.start_page.profile() == Profile(
        "Ala", ("add",), largest_number=12, question_count=5
    )
    window.start_page.question_count.setValue(3)

    # When
    qtbot.mouseClick(window.start_page.start_button, Qt.MouseButton.LeftButton)

    # Then
    assert load_profile() == Profile(
        "Ala", ("add",), largest_number=12, question_count=3
    )


def test_drill_window__new_version(qtbot: QtBot) -> None:
    """A newer release is named above the pages, linking to its page."""
    # Given
    window = DrillWindow()
    qtbot.addWidget(window)
    assert window.new_version_notice.isHidden()

    # When
    window.show_new_version(
        Release("0.5.0", "https://github.com/fizyk/tabliczka/releases/tag/v0.5.0")
    )

    # Then
    assert not window.new_version_notice.isHidden()
    assert window.new_version_notice.text() == (
        "Jest już nowa wersja programu: 0.5.0. "
        '<a href="https://github.com/fizyk/tabliczka/releases/tag/v0.5.0">'
        "Zobacz ją tutaj</a>"
    )
    assert window.new_version_notice.openExternalLinks()
    assert window.new_version_notice.focusPolicy() == Qt.FocusPolicy.StrongFocus
