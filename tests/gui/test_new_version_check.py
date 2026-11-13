"""Tests for asking GitHub whether a newer release is out."""

from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QByteArray, QObject
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from pytestqt.qtbot import QtBot

from tabliczka.releases.models import Release
from tabliczka.ui.gui.new_version_check import NewVersionCheck

RELEASE_PAGE = "https://github.com/fizyk/tabliczka/releases/tag/v99.0.0"


def reply_mock(
    body: bytes, error: QNetworkReply.NetworkError = QNetworkReply.NetworkError.NoError
) -> MagicMock:
    """Return a reply that arrived with ``body`` or failed with ``error``."""
    reply = MagicMock(spec=QNetworkReply)
    reply.error.return_value = error
    reply.readAll.return_value = QByteArray(body)
    return reply


@pytest.fixture
def check(qtbot: QtBot) -> Iterator[NewVersionCheck]:
    """Return a check whose owner lives until the test ends."""
    owner = QObject()
    yield NewVersionCheck(owner)


def test_new_version_check__start(
    monkeypatch: pytest.MonkeyPatch, check: NewVersionCheck
) -> None:
    """The check asks GitHub for the latest release and reads the reply later."""
    # Given
    get_mock = MagicMock(spec=QNetworkAccessManager.get)
    monkeypatch.setattr(check.network, "get", get_mock)

    # When
    check.start()

    # Then
    [request] = get_mock.call_args.args
    assert isinstance(request, QNetworkRequest)
    assert request.url().toString() == (
        "https://api.github.com/repos/fizyk/tabliczka/releases/latest"
    )
    assert request.transferTimeout() == 10_000
    assert request.rawHeader("User-Agent").data().startswith(b"tabliczka/")
    get_mock.return_value.finished.connect.assert_called_once()


def test_new_version_check__found(qtbot: QtBot, check: NewVersionCheck) -> None:
    """A newer release in the reply is reported."""
    # Given
    reply = reply_mock(
        b'{"tag_name": "v99.0.0", "html_url": "' + RELEASE_PAGE.encode() + b'"}'
    )

    # When
    with qtbot.waitSignal(check.found) as found:
        check.read(reply)

    # Then
    assert found.args == [Release("99.0.0", RELEASE_PAGE)]
    reply.deleteLater.assert_called_once_with()


@pytest.mark.parametrize(
    "reply",
    [
        reply_mock(
            b'{"tag_name": "v0.0.1", "html_url": '
            b'"https://github.com/fizyk/tabliczka/releases/tag/v0.0.1"}'
        ),
        reply_mock(b'{"message": "API rate limit exceeded"}'),
        reply_mock(b"<html>"),
        reply_mock(b"", QNetworkReply.NetworkError.HostNotFoundError),
        reply_mock(b"", QNetworkReply.NetworkError.OperationCanceledError),
    ],
    ids=["older", "unexpected", "not-json", "no-network", "timeout"],
)
def test_new_version_check__silent(
    qtbot: QtBot, check: NewVersionCheck, reply: MagicMock
) -> None:
    """An older release, a GitHub error or no network reports nothing."""
    # When / Then
    with qtbot.assertNotEmitted(check.found):
        check.read(reply)
