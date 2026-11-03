"""Asking a drill's questions and scoring the answers."""

from collections.abc import Iterator
from itertools import count
from random import choice

from tabliczka.exercises.models import Question
from tabliczka.practice.models import Drill


def ask_questions(drill: Drill) -> Iterator[Question]:
    """Yield questions about random operations, ``question_count`` of them if set.

    Each operation uses the drill's ``max_n`` as its largest number, or its own
    default when the drill has none.
    """
    for _ in count() if drill.question_count is None else range(drill.question_count):
        operation = choice(drill.operations)
        yield operation.generate(
            operation.default_max_n if drill.max_n is None else drill.max_n
        )


def check_answer(drill: Drill, question: Question, given: int) -> bool:
    """Record whether ``given`` answers the question, and return it."""
    correct = given == question.answer
    drill.scoreboard.record(question.operation_id, correct=correct)
    return correct
