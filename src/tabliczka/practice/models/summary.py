"""The results of a drill, reported when it ends."""

from dataclasses import dataclass

from tabliczka.practice.models.score import Score


@dataclass(frozen=True)
class Summary:
    """The drill's total, and each operation's score by operation id.

    ``scores`` follows the order the drill's operations were chosen in.
    """

    total: Score
    scores: dict[str, Score]
