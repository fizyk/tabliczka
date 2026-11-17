"""One exercise put to the learner."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    """One exercise with its expected answer.

    ``expression`` is the arithmetic asked about, such as ``2+4``. ``remainder``
    is what a division with remainder leaves over, beside the quotient in
    ``answer``, and ``None`` for a question answered with one number.
    """

    expression: str
    answer: int
    operation_id: str
    remainder: int | None = None
