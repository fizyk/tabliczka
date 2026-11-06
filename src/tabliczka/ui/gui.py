"""The window for the arithmetic drills, the program the Windows release runs."""

import sys
import traceback
from types import TracebackType

from PySide6.QtCore import QLocale, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from tabliczka.exercises.api import get_operations
from tabliczka.practice.api import Drill
from tabliczka.practice.models import Score, Summary
from tabliczka.ui.text import (
    CORRECT_FEEDBACK,
    OPERATION_HEADINGS_BY_ID,
    SUMMARY_HEADING,
    correct_count,
    greeting,
    question_text,
    wrong_count,
    wrong_feedback,
)

WINDOW_TITLE = "Tabliczka"
ERROR_MESSAGE = "Coś poszło nie tak. Zamknij program i uruchom go jeszcze raz."
LARGEST_NUMBER_LIMIT = 1000
QUESTION_COUNT_LIMIT = 1000
CORRECT_COLOUR = "green"
WRONG_COLOUR = "red"


def coloured(text: str, colour: str) -> str:
    """Return the text as rich text in the colour."""
    return f'<span style="color: {colour}">{text}</span>'


def summary_html(summary: Summary) -> str:
    """Return the totals, then the score of each operation, as rich text."""
    sections = [(SUMMARY_HEADING, summary.total)] + [
        (f"{OPERATION_HEADINGS_BY_ID[operation_id]}:", score)
        for operation_id, score in summary.scores.items()
    ]
    return "<hr>".join(
        "<br>".join([heading, *score_lines(score)]) for heading, score in sections
    )


def score_lines(score: Score) -> list[str]:
    """Return the correct count, then the wrong count when there are wrong answers."""
    lines = [coloured(correct_count(score), CORRECT_COLOUR)]
    if score.wrong:
        lines.append(coloured(wrong_count(score), WRONG_COLOUR))
    return lines


def whole_number_validator(parent: QWidget) -> QIntValidator:
    """Return a validator of whole numbers typed without group separators."""
    validator = QIntValidator(parent)
    locale = validator.locale()
    locale.setNumberOptions(QLocale.NumberOption.RejectGroupSeparator)
    validator.setLocale(locale)
    return validator


class StartPage(QWidget):
    """Asks for the learner's name and the drill.

    The drill is the operations, the largest number and the number of questions.
    """

    def __init__(self) -> None:
        """Lay out the questions, with every operation chosen."""
        super().__init__()
        self.name = QLineEdit()
        self.operation_boxes = {
            operation_id: QCheckBox(heading)
            for operation_id, heading in OPERATION_HEADINGS_BY_ID.items()
        }
        self.max_n = QSpinBox()
        self.max_n.setMaximum(LARGEST_NUMBER_LIMIT)
        self.max_n.setSpecialValueText("domyślna")
        self.question_count = QSpinBox()
        self.question_count.setMaximum(QUESTION_COUNT_LIMIT)
        self.question_count.setSpecialValueText("bez limitu")
        self.start_button = QPushButton("Zaczynamy!")

        operations = QWidget()
        operations_layout = QVBoxLayout(operations)
        for box in self.operation_boxes.values():
            box.setChecked(True)
            box.toggled.connect(self.update_limits)
            operations_layout.addWidget(box)
        layout = QFormLayout(self)
        layout.addRow("Jak masz na imię?", self.name)
        layout.addRow("Co ćwiczymy?", operations)
        layout.addRow("Największa liczba:", self.max_n)
        layout.addRow("Liczba pytań:", self.question_count)
        layout.addRow(self.start_button)

        self.name.textChanged.connect(self.update_limits)
        self.name.returnPressed.connect(self.start_button.click)
        self.update_limits()

    def learner_name(self) -> str:
        """Return the typed name without surrounding spaces."""
        return self.name.text().strip()

    def operation_ids(self) -> list[str]:
        """Return the ids of the chosen operations."""
        return [
            operation_id
            for operation_id, box in self.operation_boxes.items()
            if box.isChecked()
        ]

    def chosen_max_n(self) -> int | None:
        """Return the chosen largest number, or ``None`` for each operation's own."""
        value = self.max_n.value()
        return None if value == self.max_n.minimum() else value

    def chosen_question_count(self) -> int | None:
        """Return the chosen number of questions, or ``None`` for no limit."""
        return self.question_count.value() or None

    def update_limits(self) -> None:
        """Keep the largest number within the chosen operations' limits.

        Allow starting only with a name and at least one operation.
        """
        operation_ids = self.operation_ids()
        smallest = max(
            (operation.min_max_n for operation in get_operations(operation_ids)),
            default=1,
        )
        chosen = self.chosen_max_n()
        self.max_n.setMinimum(smallest - 1)
        self.max_n.setValue(
            self.max_n.minimum() if chosen is None else max(chosen, smallest)
        )
        self.start_button.setEnabled(bool(self.learner_name() and operation_ids))


class QuestionPage(QWidget):
    """Asks a drill's questions one at a time and says whether each answer is right."""

    finished = Signal()

    def __init__(self, name: str, drill: Drill, feedback: QLabel) -> None:
        """Ask the drill's first question."""
        super().__init__()
        self.drill = drill
        self.feedback = feedback
        self.questions = drill.questions()
        self.question = next(self.questions)
        self.question_label = QLabel(question_text(self.question))
        self.answer = QLineEdit()
        self.answer.setValidator(whole_number_validator(self.answer))
        self.stop_button = QPushButton("Koniec")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(greeting(name)))
        layout.addWidget(self.question_label)
        layout.addWidget(self.answer)
        layout.addWidget(self.stop_button)

        self.answer.returnPressed.connect(self.submit)
        self.stop_button.clicked.connect(lambda: self.finished.emit())

    def submit(self) -> None:
        """Score the typed answer, then ask the next question or finish."""
        if not self.answer.hasAcceptableInput():
            return
        if self.drill.check_answer(self.question, int(self.answer.text())):
            self.feedback.setText(coloured(CORRECT_FEEDBACK, CORRECT_COLOUR))
        else:
            self.feedback.setText(coloured(wrong_feedback(self.question), WRONG_COLOUR))
        self.answer.clear()
        question = next(self.questions, None)
        if question is None:
            self.finished.emit()
            return
        self.question = question
        self.question_label.setText(question_text(question))


class SummaryPage(QLabel):
    """Shows a drill's summary."""

    def __init__(self, summary: Summary) -> None:
        """Show the totals, then the score of each operation."""
        super().__init__(summary_html(summary))


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
        drill = Drill(
            self.start_page.operation_ids(),
            max_n=self.start_page.chosen_max_n(),
            question_count=self.start_page.chosen_question_count(),
        )
        page = QuestionPage(self.start_page.learner_name(), drill, self.feedback)
        page.finished.connect(lambda: self.show_page(SummaryPage(drill.summary())))
        self.show_page(page)
        page.answer.setFocus()

    def show_page(self, page: QWidget) -> None:
        """Replace the current page with ``page``."""
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)


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
