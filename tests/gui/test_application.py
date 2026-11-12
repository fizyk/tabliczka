"""Tests for running the window and showing unexpected errors."""

import sys
from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QApplication, QMessageBox

from tabliczka.ui.gui.application import main, show_error
from tabliczka.ui.gui.new_version_check import NewVersionCheck


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


@pytest.fixture
def application_mock(monkeypatch: pytest.MonkeyPatch, qapp: QApplication) -> MagicMock:
    """Return the application ``main`` creates, whose run ends at once."""
    application_mock = MagicMock(spec=QApplication)
    application_mock.return_value.exec.return_value = 0
    monkeypatch.setattr("tabliczka.ui.gui.application.QApplication", application_mock)
    monkeypatch.setattr(sys, "excepthook", sys.excepthook)
    return application_mock


@pytest.fixture
def check_mock(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Return the new version check ``main`` creates."""
    check_mock = MagicMock(spec=NewVersionCheck)
    monkeypatch.setattr("tabliczka.ui.gui.application.NewVersionCheck", check_mock)
    return check_mock


def test_main(application_mock: MagicMock, check_mock: MagicMock) -> None:
    """The window opens and unexpected errors are shown until it closes."""
    # When
    with pytest.raises(SystemExit) as exit_info:
        main()

    # Then
    assert exit_info.value.code == 0
    assert sys.excepthook is show_error
    check_mock.assert_not_called()


def test_main__packaged(
    monkeypatch: pytest.MonkeyPatch, application_mock: MagicMock, check_mock: MagicMock
) -> None:
    """The packaged program also asks whether a newer release is out."""
    # Given
    monkeypatch.setattr(sys, "frozen", True, raising=False)

    # When
    with pytest.raises(SystemExit):
        main()

    # Then
    [window] = check_mock.call_args.args
    check_mock.return_value.found.connect.assert_called_once_with(
        window.show_new_version
    )
    check_mock.return_value.start.assert_called_once_with()
