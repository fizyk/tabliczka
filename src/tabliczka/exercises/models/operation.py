"""An arithmetic skill a drill can ask questions about."""

from typing import Protocol

from tabliczka.exercises.models.question import Question


class Operation(Protocol):
    """An arithmetic skill that generates questions.

    Each operation decides which number its largest number limits, how large
    that number is when the drill does not choose one, and how small it can be.
    """

    id: str
    default_largest_number: int
    smallest_largest_number: int

    def generate(self, largest_number: int) -> Question:
        """Return a question whose limited number is at most ``largest_number``."""
        ...
