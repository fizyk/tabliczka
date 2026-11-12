"""Asking GitHub in the background whether a newer release is out."""

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from tabliczka import __version__
from tabliczka.core.constants import APPLICATION_NAME
from tabliczka.releases import LATEST_RELEASE_URL, is_newer, read_release
from tabliczka.releases.models import Release

TIMEOUT_MILLISECONDS = 10_000


class NewVersionCheck(QObject):
    """Asks GitHub for the latest release without blocking the window.

    Reports a release newer than the running program with ``found``. Says nothing
    when there is no network, GitHub fails or its reply is unexpected.
    """

    found = Signal(Release)

    def __init__(self, parent: QObject) -> None:
        """Prepare the network access, owned by ``parent``."""
        super().__init__(parent)
        self.network = QNetworkAccessManager(self)

    def start(self) -> None:
        """Send the request; the reply is read when it arrives."""
        request = QNetworkRequest(QUrl(LATEST_RELEASE_URL))
        request.setTransferTimeout(TIMEOUT_MILLISECONDS)
        request.setRawHeader(b"Accept", b"application/vnd.github+json")
        request.setRawHeader(
            b"User-Agent", f"{APPLICATION_NAME}/{__version__}".encode()
        )
        reply = self.network.get(request)
        reply.finished.connect(lambda: self.read(reply))

    def read(self, reply: QNetworkReply) -> None:
        """Report the release in the reply when it is newer than the program."""
        reply.deleteLater()
        if reply.error() != QNetworkReply.NetworkError.NoError:
            return
        try:
            release = read_release(bytes(reply.readAll().data()))
            newer = is_newer(release, __version__)
        except ValueError:
            return
        if newer:
            self.found.emit(release)
