"""The first page, asking for the learner's name and the drill."""

from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from tabliczka.exercises.api import get_operations
from tabliczka.profiles.models import Profile
from tabliczka.ui.gui.text import (
    DEFAULT_LARGEST_NUMBER_TEXT,
    LARGEST_NUMBER_LABEL,
    NAME_LABEL,
    NO_QUESTION_COUNT_TEXT,
    OPERATIONS_LABEL,
    QUESTION_COUNT_LABEL,
    START_BUTTON_TEXT,
)
from tabliczka.ui.text import OPERATION_HEADINGS_BY_ID

LARGEST_NUMBER_LIMIT = 1000
QUESTION_COUNT_LIMIT = 1000


class StartPage(QWidget):
    """Asks for the learner's name and the drill.

    The drill is the operations, the largest number and the number of questions.
    """

    def __init__(self, profile: Profile) -> None:
        """Lay out the questions, showing the profile ready to change."""
        super().__init__()
        self.name = QLineEdit(profile.name)
        self.operation_boxes = {
            operation_id: QCheckBox(heading)
            for operation_id, heading in OPERATION_HEADINGS_BY_ID.items()
        }
        self.largest_number = QSpinBox()
        self.largest_number.setMaximum(LARGEST_NUMBER_LIMIT)
        self.largest_number.setSpecialValueText(DEFAULT_LARGEST_NUMBER_TEXT)
        self.question_count = QSpinBox()
        self.question_count.setMaximum(QUESTION_COUNT_LIMIT)
        self.question_count.setSpecialValueText(NO_QUESTION_COUNT_TEXT)
        self.question_count.setValue(profile.question_count or 0)
        self.start_button = QPushButton(START_BUTTON_TEXT)

        operations = QWidget()
        operations_layout = QVBoxLayout(operations)
        for operation_id, box in self.operation_boxes.items():
            box.setChecked(operation_id in profile.operation_ids)
            box.toggled.connect(self.update_limits)
            operations_layout.addWidget(box)
        layout = QFormLayout(self)
        layout.addRow(NAME_LABEL, self.name)
        layout.addRow(OPERATIONS_LABEL, operations)
        layout.addRow(LARGEST_NUMBER_LABEL, self.largest_number)
        layout.addRow(QUESTION_COUNT_LABEL, self.question_count)
        layout.addRow(self.start_button)

        self.name.textChanged.connect(self.update_limits)
        self.name.returnPressed.connect(self.start_button.click)
        self.update_limits()
        self.largest_number.setValue(profile.largest_number or 0)

    def profile(self) -> Profile:
        """Return the typed name and the chosen operations and limits."""
        return Profile(
            name=self.learner_name(),
            operation_ids=tuple(self.operation_ids()),
            largest_number=self.chosen_largest_number(),
            question_count=self.chosen_question_count(),
        )

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

    def chosen_largest_number(self) -> int | None:
        """Return the chosen largest number, or ``None`` for each operation's own."""
        value = self.largest_number.value()
        return None if value == self.largest_number.minimum() else value

    def chosen_question_count(self) -> int | None:
        """Return the chosen number of questions, or ``None`` for no limit."""
        return self.question_count.value() or None

    def update_limits(self) -> None:
        """Keep the largest number within the chosen operations' limits.

        Allow starting only with a name and at least one operation.
        """
        operation_ids = self.operation_ids()
        smallest = max(
            (
                operation.smallest_largest_number
                for operation in get_operations(operation_ids)
            ),
            default=1,
        )
        chosen = self.chosen_largest_number()
        self.largest_number.setMinimum(smallest - 1)
        self.largest_number.setValue(
            self.largest_number.minimum() if chosen is None else max(chosen, smallest)
        )
        self.start_button.setEnabled(bool(self.learner_name() and operation_ids))
