"""The learner's name and drill, kept between runs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    """The learner's name and the drill: operations, largest number and questions.

    ``max_n`` is ``None`` for each operation's own largest number, and
    ``question_count`` is ``None`` for no limit.
    """

    name: str
    operation_ids: tuple[str, ...]
    max_n: int | None
    question_count: int | None
