"""The drill loop, the learner's answers and the summary."""

from collections.abc import Sequence
from contextlib import suppress
from itertools import count
from random import choice

import click
from click import Abort

from tabliczka.exercises.models import Operation
from tabliczka.practice.models import Score, Scoreboard

STOP_WORD = "koniec"


class LearnerAnswer(click.ParamType):
    """What the learner types in answer: a whole number, or the stop word."""

    name = "answer"

    def convert(
        self, value: object, param: click.Parameter | None, ctx: click.Context | None
    ) -> int | None:
        """Return the typed number, or ``None`` for the stop word."""
        if isinstance(value, int):
            return value
        text = str(value).strip()
        if text.lower() == STOP_WORD:
            return None
        try:
            return int(text)
        except ValueError:
            self.fail(f"Wpisz liczbę albo „{STOP_WORD}”.", param, ctx)


LEARNER_ANSWER = LearnerAnswer()


def print_score(score: Score) -> None:
    """Print the correct count, then the wrong count when there are wrong answers."""
    click.echo(click.style(f"{score.correct} - dobrze", fg="green"))
    if score.wrong:
        click.echo(click.style(f"{score.wrong} - źle", fg="red"))


def print_summary(scoreboard: Scoreboard, operations: Sequence[Operation]) -> None:
    """Print the totals, then the score of each operation."""
    click.echo("\n")
    click.echo("=" * 20)
    click.echo("Twój wynik to:")
    print_score(scoreboard.total(operation.id for operation in operations))
    click.echo("=" * 20)

    for index, operation in enumerate(operations):
        if index:
            click.echo("=" * 20)
        click.echo(operation.heading)
        print_score(scoreboard.score(operation.id))


def run_drill(
    operations: Sequence[Operation],
    *,
    max_n: int | None = None,
    question_count: int | None = None,
) -> None:
    """Ask questions until the learner stops, aborts or answers ``question_count``.

    Each operation uses ``max_n`` as its largest number, or its own default when
    ``max_n`` is not given. Then print the summary.
    """
    scoreboard = Scoreboard()
    click.echo(f"Wpisz „{STOP_WORD}”, żeby zakończyć.")
    with suppress(Abort):
        for _ in count() if question_count is None else range(question_count):
            operation = choice(operations)
            question = operation.generate(
                operation.default_max_n if max_n is None else max_n
            )
            answer = click.prompt(question.prompt, type=LEARNER_ANSWER)
            if answer is None:
                break
            correct = answer == question.answer
            if correct:
                click.echo(click.style("Dobrze!", fg="green"))
            else:
                click.echo(
                    click.style(
                        f"Niestety, źle, prawidłowy wynik to {question.answer}.",
                        fg="red",
                    )
                )
            scoreboard.record(question.operation_id, correct=correct)
    print_summary(scoreboard, operations)
