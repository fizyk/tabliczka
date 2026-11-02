"""An arithmetic skill a drill can ask questions about."""

from typing import Protocol

from tabliczka.exercises.models.question import Question


class Operation(Protocol):
    """An arithmetic skill that generates questions.

    Each operation decides which number its largest number limits, and how large
    that number is when the drill does not choose one.
    """

    id: str
    heading: str
    default_max_n: int

    def generate(self, max_n: int) -> Question:
        """Return a question whose limited number is at most ``max_n``."""
        ...
