"""The window that moves from the start page to the questions to the summary."""

from PySide6.QtWidgets import QLabel, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from tabliczka.practice.api import Drill
from tabliczka.profiles.api import load_profile, save_profile
from tabliczka.ui.gui.pages.question import QuestionPage
from tabliczka.ui.gui.pages.start import StartPage
from tabliczka.ui.gui.pages.summary import SummaryPage
from tabliczka.ui.gui.rich_text import feedback_html
from tabliczka.ui.gui.text import WINDOW_TITLE


class DrillWindow(QMainWindow):
    """Asks for the name and the drill, runs the drill, then shows the summary.

    The start page shows the profile saved at the last start, and each start saves
    it. The feedback on the last answer stays below the pages.
    """

    def __init__(self) -> None:
        """Show the start page, filled with the saved profile if there is one."""
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.start_page = StartPage()
        profile = load_profile()
        if profile is not None:
            self.start_page.fill(profile)
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
        """Save the chosen profile, start the drill and ask its first question."""
        profile = self.start_page.profile()
        save_profile(profile)
        drill = Drill(
            profile.operation_ids,
            max_n=profile.max_n,
            question_count=profile.question_count,
        )
        page = QuestionPage(profile.name, drill)
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
