"""One exercise put to the learner."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    """One exercise with its expected answer."""

    prompt: str
    answer: int
    operation_id: str
