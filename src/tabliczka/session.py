"""Drill sessions: asking questions and keeping the score."""

from collections.abc import Sequence
from contextlib import suppress
from random import choice

import click
from click import Abort

from tabliczka.operations import Operation

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


class Scoreboard:
    """Correct and wrong answer counts per operation."""

    def __init__(self) -> None:
        """Start with no answers recorded."""
        self.scores: dict[str, dict[str, int]] = {}

    def record(self, operation_id: str, *, correct: bool) -> None:
        """Count one answer for an operation."""
        score = self.scores.setdefault(operation_id, {"ok": 0, "bad": 0})
        score["ok" if correct else "bad"] += 1

    def print_summary(self, operations: Sequence[Operation]) -> None:
        """Print the totals, then the score of each operation."""
        ok = sum(
            self.scores.get(operation.id, {}).get("ok", 0) for operation in operations
        )
        bad = sum(
            self.scores.get(operation.id, {}).get("bad", 0) for operation in operations
        )

        click.echo("\n")
        click.echo("=" * 20)
        click.echo("Twój wynik to:")
        click.echo(click.style(f"{ok} - dobrze", fg="green"))
        if bad:
            click.echo(click.style(f"{bad} - źle", fg="red"))
        click.echo("=" * 20)

        for index, operation in enumerate(operations):
            if index:
                click.echo("=" * 20)
            score = self.scores.get(operation.id, {})
            click.echo(operation.heading)
            click.echo(click.style(f"{score.get('ok', 0)} - dobrze", fg="green"))
            if bad:
                click.echo(click.style(f"{score.get('bad', 0)} - źle", fg="red"))


def run_drill(
    operations: Sequence[Operation], *, min_n: int = 1, max_n: int = 10
) -> None:
    """Ask questions until the learner stops or aborts, then print the summary."""
    scoreboard = Scoreboard()
    click.echo(f"Wpisz „{STOP_WORD}”, żeby zakończyć.")
    with suppress(Abort):
        while True:
            operation = choice(operations)
            question = operation.generate(min_n=min_n, max_n=max_n)
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
    scoreboard.print_summary(operations)
