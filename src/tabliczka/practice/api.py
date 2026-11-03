"""Running a drill: asking its questions, scoring the answers, summing up."""

from collections.abc import Iterator, Sequence

from tabliczka.exercises.api import get_operations
from tabliczka.exercises.models import Question
from tabliczka.practice import service
from tabliczka.practice.models import Scoreboard, Summary


class Drill:
    """A run of questions over chosen operations, and its score."""

    def __init__(
        self,
        operation_ids: Sequence[str],
        *,
        max_n: int | None = None,
        question_count: int | None = None,
    ) -> None:
        """Start a drill of the operations with the given ids, with no answers yet."""
        self.operations = get_operations(operation_ids)
        self.max_n = max_n
        self.question_count = question_count
        self.scoreboard = Scoreboard()

    def questions(self) -> Iterator[Question]:
        """Yield the drill's questions until it has asked ``question_count``, if set."""
        return service.ask_questions(
            self.operations, max_n=self.max_n, question_count=self.question_count
        )

    def check_answer(self, question: Question, given: int) -> bool:
        """Record whether ``given`` answers the question, and return it."""
        return service.check_answer(self.scoreboard, question, given)

    def summary(self) -> Summary:
        """Return the drill's total and each operation's score so far."""
        return service.summarise(self.scoreboard, self.operations)
