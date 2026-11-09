"""Asking a drill's questions, scoring the answers and summing the scores."""

from collections.abc import Iterator, Sequence
from itertools import count
from random import choice

from tabliczka.exercises.models import Operation, Question
from tabliczka.practice.models import Score, Scoreboard, Summary


def check_drill(
    operations: Sequence[Operation],
    *,
    largest_number: int | None,
    question_count: int | None,
) -> None:
    """Reject a drill that could not ask its questions."""
    if not operations:
        raise ValueError("A drill needs operation ids. Give at least one.")
    too_small_for = [
        operation
        for operation in operations
        if largest_number is not None
        and largest_number < operation.smallest_largest_number
    ]
    if too_small_for:
        smallest_allowed = max(
            operation.smallest_largest_number for operation in too_small_for
        )
        raise ValueError(
            f"The largest_number {largest_number} is too small for operation ids "
            f"{[operation.id for operation in too_small_for]}. "
            f"Give {smallest_allowed} or more, or None."
        )
    if question_count is not None and question_count < 1:
        raise ValueError(
            f"The question_count {question_count} is below 1. Give 1 or more, or None."
        )


def ask_questions(
    operations: Sequence[Operation],
    *,
    largest_number: int | None,
    question_count: int | None,
) -> Iterator[Question]:
    """Yield questions about random operations, ``question_count`` of them if set.

    Each operation uses ``largest_number``, or its own default when it is not given.
    """
    for _ in count() if question_count is None else range(question_count):
        operation = choice(operations)
        yield operation.generate(
            operation.default_largest_number
            if largest_number is None
            else largest_number
        )


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
