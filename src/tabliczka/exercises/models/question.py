"""One exercise put to the learner."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    """One exercise with its expected answer.

    ``expression`` is the arithmetic asked about, such as ``2+4``.
    """

    expression: str
    answer: int
    operation_id: str
