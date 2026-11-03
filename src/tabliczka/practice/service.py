"""Asking a drill's questions, scoring the answers and summing the scores."""

from collections.abc import Iterator, Sequence
from itertools import count
from random import choice

from tabliczka.exercises.models import Operation, Question
from tabliczka.practice.models import Score, Scoreboard, Summary


def ask_questions(
    operations: Sequence[Operation],
    *,
    max_n: int | None,
    question_count: int | None,
) -> Iterator[Question]:
    """Yield questions about random operations, ``question_count`` of them if set.

    Each operation uses ``max_n`` as its largest number, or its own default when
    ``max_n`` is not given.
    """
    for _ in count() if question_count is None else range(question_count):
        operation = choice(operations)
        yield operation.generate(operation.default_max_n if max_n is None else max_n)


def check_answer(scoreboard: Scoreboard, question: Question, given: int) -> bool:
    """Record whether ``given`` answers the question, and return it."""
    correct = given == question.answer
    scoreboard.record(question.operation_id, correct=correct)
    return correct


def summarise(scoreboard: Scoreboard, operations: Sequence[Operation]) -> Summary:
    """Return each operation's score and their total."""
    scores = {operation.id: scoreboard.score(operation.id) for operation in operations}
    total = Score(
        correct=sum(score.correct for score in scores.values()),
        wrong=sum(score.wrong for score in scores.values()),
    )
    return Summary(total, scores)
