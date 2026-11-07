"""The page that asks a drill's questions one at a time."""

from PySide6.QtCore import QLocale, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from tabliczka.exercises.models import Question
from tabliczka.practice.api import Drill
from tabliczka.ui.gui.text import STOP_BUTTON_TEXT
from tabliczka.ui.text import greeting, question_text


def whole_number_validator(parent: QWidget) -> QIntValidator:
    """Return a validator of whole numbers typed without group separators."""
    validator = QIntValidator(parent)
    locale = validator.locale()
    locale.setNumberOptions(QLocale.NumberOption.RejectGroupSeparator)
    validator.setLocale(locale)
    return validator


class QuestionPage(QWidget):
    """Asks a drill's questions one at a time.

    Reports each scored answer with ``answered``: the question and whether the
    answer was correct.
    """

    answered = Signal(Question, bool)
    finished = Signal()

    def __init__(self, name: str, drill: Drill) -> None:
        """Ask the drill's first question."""
        super().__init__()
        self.drill = drill
        self.questions = drill.questions()
        self.question = next(self.questions)
        self.question_label = QLabel(question_text(self.question))
        self.given = QLineEdit()
        self.given.setValidator(whole_number_validator(self.given))
        self.stop_button = QPushButton(STOP_BUTTON_TEXT)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(greeting(name)))
        layout.addWidget(self.question_label)
        layout.addWidget(self.given)
        layout.addWidget(self.stop_button)

        self.given.returnPressed.connect(self.submit)
        self.stop_button.clicked.connect(lambda: self.finished.emit())

    def submit(self) -> None:
        """Score the typed answer, then ask the next question or finish."""
        if not self.given.hasAcceptableInput():
            return
        correct = self.drill.check_answer(self.question, int(self.given.text()))
        self.answered.emit(self.question, correct)
        self.given.clear()
        question = next(self.questions, None)
        if question is None:
            self.finished.emit()
            return
        self.question = question
        self.question_label.setText(question_text(question))
