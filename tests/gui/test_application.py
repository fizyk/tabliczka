"""Tests for running the window and showing unexpected errors."""

import sys
from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QApplication, QMessageBox

from tabliczka.ui.gui.application import main, show_error


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
    monkeypatch.setattr("tabliczka.ui.gui.application.QApplication", application_mock)
    monkeypatch.setattr(sys, "excepthook", sys.excepthook)

    # When
    with pytest.raises(SystemExit) as exit_info:
        main()

    # Then
    assert exit_info.value.code == 0
    assert sys.excepthook is show_error
