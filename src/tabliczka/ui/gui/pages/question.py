"""The page that asks a drill's questions one at a time."""

from PySide6.QtCore import QLocale, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from tabliczka.exercises.models import Question
from tabliczka.practice import Drill
from tabliczka.ui.gui.text import STOP_BUTTON_TEXT
from tabliczka.ui.text import REMAINDER_WORD, greeting, question_text


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
    answer was correct. A division with remainder asks for the remainder in a
    second field.
    """

    answered = Signal(Question, bool)
    finished = Signal()

    def __init__(self, name: str, drill: Drill) -> None:
        """Ask the drill's first question."""
        super().__init__()
        self.drill = drill
        self.questions = drill.questions()
        self.question_label = QLabel()
        self.given_answer = QLineEdit()
        self.given_answer.setValidator(whole_number_validator(self.given_answer))
        self.remainder_label = QLabel(REMAINDER_WORD)
        self.given_remainder = QLineEdit()
        self.given_remainder.setValidator(whole_number_validator(self.given_remainder))
        self.stop_button = QPushButton(STOP_BUTTON_TEXT)

        answer_row = QHBoxLayout()
        answer_row.addWidget(self.given_answer)
        answer_row.addWidget(self.remainder_label)
        answer_row.addWidget(self.given_remainder)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(greeting(name)))
        layout.addWidget(self.question_label)
        layout.addLayout(answer_row)
        layout.addWidget(self.stop_button)

        self.given_answer.returnPressed.connect(self.submit)
        self.given_remainder.returnPressed.connect(self.submit)
        self.stop_button.clicked.connect(lambda: self.finished.emit())
        self.show_question(next(self.questions))

    def asks_remainder(self) -> bool:
        """Return whether the current question asks for a remainder."""
        return self.question.remainder is not None

    def show_question(self, question: Question) -> None:
        """Show the question, with the remainder field only when it asks for one."""
        self.question = question
        self.question_label.setText(question_text(question))
        self.remainder_label.setVisible(self.asks_remainder())
        self.given_remainder.setVisible(self.asks_remainder())

    def submit(self) -> None:
        """Score the typed answer, then ask the next question or finish.

        Until every field the question asks for holds a whole number, move to the
        first one that does not.
        """
        fields = [self.given_answer]
        if self.asks_remainder():
            fields.append(self.given_remainder)
        unanswered_field = next(
            (field for field in fields if not field.hasAcceptableInput()), None
        )
        if unanswered_field is not None:
            unanswered_field.setFocus()
            return
        correct = self.drill.check_answer(
            self.question,
            int(self.given_answer.text()),
            given_remainder=(
                int(self.given_remainder.text()) if self.asks_remainder() else None
            ),
        )
        self.answered.emit(self.question, correct)
        self.given_answer.clear()
        self.given_remainder.clear()
        question = next(self.questions, None)
        if question is None:
            self.finished.emit()
            return
        self.show_question(question)
        self.given_answer.setFocus()
