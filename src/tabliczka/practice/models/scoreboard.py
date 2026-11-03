"""The record of a drill's results."""

from tabliczka.practice.models.score import Score


class Scoreboard:
    """Correct and wrong answer counts per operation."""

    def __init__(self) -> None:
        """Start with no answers recorded."""
        self.scores: dict[str, Score] = {}

    def record(self, operation_id: str, *, correct: bool) -> None:
        """Count one answer for an operation."""
        score = self.scores.setdefault(operation_id, Score())
        if correct:
            score.correct += 1
        else:
            score.wrong += 1

    def score(self, operation_id: str) -> Score:
        """Return the score of one operation, zero when it has no answers."""
        return self.scores.get(operation_id, Score())
