"""The window that moves from the start page to the questions to the summary."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from tabliczka.practice import Drill
from tabliczka.profiles import load_profile, save_profile
from tabliczka.releases.models import Release
from tabliczka.ui.gui.pages.question import QuestionPage
from tabliczka.ui.gui.pages.start import StartPage
from tabliczka.ui.gui.pages.summary import SummaryPage
from tabliczka.ui.gui.rich_text import feedback_html, new_version_html
from tabliczka.ui.gui.text import WINDOW_TITLE


class DrillWindow(QMainWindow):
    """Asks for the name and the drill, runs the drill, then shows the summary.

    The start page shows the profile saved at the last start, and each start saves
    it. The feedback on the last answer stays below the pages, and the notice of a
    newer release, once there is one, above them.
    """

    def __init__(self) -> None:
        """Show the start page, filled with the saved or an empty profile."""
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.start_page = StartPage(load_profile())
        self.pages = QStackedWidget()
        self.pages.addWidget(self.start_page)
        self.feedback = QLabel()
        self.new_version_notice = QLabel()
        self.new_version_notice.setOpenExternalLinks(True)
        self.new_version_notice.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse
            | Qt.TextInteractionFlag.LinksAccessibleByKeyboard
        )
        self.new_version_notice.hide()

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.new_version_notice)
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
            largest_number=profile.largest_number,
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

    def show_new_version(self, release: Release) -> None:
        """Show the notice of a newer release above the pages."""
        self.new_version_notice.setText(new_version_html(release))
        self.new_version_notice.show()
