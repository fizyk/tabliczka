"""Running a drill: asking its questions, scoring the answers, summing up."""

from collections.abc import Iterator, Sequence

from tabliczka.exercises import get_operations
from tabliczka.exercises.models import Question
from tabliczka.practice import service
from tabliczka.practice.models import Scoreboard, Summary


class Drill:
    """A run of questions over chosen operations, and its score."""

    def __init__(
        self,
        operation_ids: Sequence[str],
        *,
        largest_number: int | None = None,
        question_count: int | None = None,
    ) -> None:
        """Start a drill of the operations with the given ids, with no answers yet.

        Reject no operation ids, a ``largest_number`` below an operation's
        ``smallest_largest_number`` and a ``question_count`` below 1.
        """
        self.operations = get_operations(operation_ids)
        service.check_drill(
            self.operations,
            largest_number=largest_number,
            question_count=question_count,
        )
        self.largest_number = largest_number
        self.question_count = question_count
        self.scoreboard = Scoreboard()

    def questions(self) -> Iterator[Question]:
        """Yield the drill's questions until it has asked ``question_count``, if set."""
        return service.ask_questions(
            self.operations,
            largest_number=self.largest_number,
            question_count=self.question_count,
        )

    def check_answer(
        self,
        question: Question,
        given_answer: int,
        *,
        given_remainder: int | None = None,
    ) -> bool:
        """Record and return whether the given answer and remainder are right.

        Reject a remainder for a question with none, and no remainder for one with one.
        """
        return service.check_answer(
            self.scoreboard, question, given_answer, given_remainder=given_remainder
        )

    def summary(self) -> Summary:
        """Return the drill's total and each operation's score so far."""
        return service.summarise(self.scoreboard, self.operations)
