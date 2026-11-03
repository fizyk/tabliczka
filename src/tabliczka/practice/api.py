"""Starting a drill, asking its questions and scoring the answers."""

from collections.abc import Iterator, Sequence

from tabliczka.exercises.api import get_operations
from tabliczka.exercises.models import Question
from tabliczka.practice import service
from tabliczka.practice.models import Drill


def start_drill(
    operation_ids: Sequence[str],
    *,
    max_n: int | None = None,
    question_count: int | None = None,
) -> Drill:
    """Return a drill of the operations with the given ids, with no answers yet."""
    return Drill(
        get_operations(operation_ids), max_n=max_n, question_count=question_count
    )


def ask_questions(drill: Drill) -> Iterator[Question]:
    """Yield the drill's questions until it has asked ``question_count``, if set."""
    return service.ask_questions(drill)


def check_answer(drill: Drill, question: Question, given: int) -> bool:
    """Record whether ``given`` answers the question, and return it."""
    return service.check_answer(drill, question, given)
