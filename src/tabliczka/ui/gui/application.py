"""Running the window, and showing unexpected errors in a message."""

import sys
import traceback
from types import TracebackType

from PySide6.QtWidgets import QApplication, QMessageBox

from tabliczka.ui.gui.drill_window import DrillWindow
from tabliczka.ui.gui.text import ERROR_MESSAGE, WINDOW_TITLE


def show_error(
    error_type: type[BaseException],
    error: BaseException,
    error_traceback: TracebackType | None,
) -> None:
    """Show an unexpected error in a message, with its traceback in the details."""
    sys.__excepthook__(error_type, error, error_traceback)
    message = QMessageBox(QMessageBox.Icon.Critical, WINDOW_TITLE, ERROR_MESSAGE)
    message.setDetailedText(
        "".join(traceback.format_exception(error_type, error, error_traceback))
    )
    message.exec()


def main() -> None:
    """Open the window and run until it closes."""
    application = QApplication(sys.argv)
    sys.excepthook = show_error
    window = DrillWindow()
    window.show()
    sys.exit(application.exec())
