"""The window that moves from the start page to the questions to the summary."""

from PySide6.QtWidgets import QLabel, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from tabliczka.practice.api import Drill
from tabliczka.ui.gui.pages.question import QuestionPage
from tabliczka.ui.gui.pages.start import StartPage
from tabliczka.ui.gui.pages.summary import SummaryPage
from tabliczka.ui.gui.rich_text import feedback_html
from tabliczka.ui.gui.text import WINDOW_TITLE


class DrillWindow(QMainWindow):
    """Asks for the name and the drill, runs the drill, then shows the summary.

    The feedback on the last answer stays below the pages.
    """

    def __init__(self) -> None:
        """Show the start page."""
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.start_page = StartPage()
        self.pages = QStackedWidget()
        self.pages.addWidget(self.start_page)
        self.feedback = QLabel()

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.pages)
        layout.addWidget(self.feedback)
        self.setCentralWidget(central)

        self.start_page.start_button.clicked.connect(self.start_drill)

    def start_drill(self) -> None:
        """Start the chosen drill and ask its first question."""
        settings = self.start_page.settings()
        drill = Drill(
            settings.operation_ids,
            max_n=settings.max_n,
            question_count=settings.question_count,
        )
        page = QuestionPage(settings.name, drill)
        page.answered.connect(
            lambda question, correct: self.feedback.setText(
                feedback_html(question, correct=correct)
            )
        )
        page.finished.connect(lambda: self.show_page(SummaryPage(drill.summary())))
        self.show_page(page)
        page.given.setFocus()

    def show_page(self, page: QWidget) -> None:
        """Replace the current page with ``page``."""
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)
