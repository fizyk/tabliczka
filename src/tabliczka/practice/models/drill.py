"""A run of questions put to the learner."""

from collections.abc import Sequence
from dataclasses import dataclass, field

from tabliczka.exercises.models import Operation
from tabliczka.practice.models.scoreboard import Scoreboard


@dataclass
class Drill:
    """The operations a drill asks about, its limits and its score."""

    operations: Sequence[Operation]
    max_n: int | None = None
    question_count: int | None = None
    scoreboard: Scoreboard = field(default_factory=Scoreboard)
