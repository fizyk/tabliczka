"""Drill sessions: asking questions and keeping the score."""

from collections.abc import Sequence
from random import choice

import click
from click import Abort

from tabliczka.operations import Operation


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
    """Ask questions until the learner aborts, then print the summary."""
    scoreboard = Scoreboard()
    try:
        while True:
            operation = choice(operations)
            question = operation.generate(min_n=min_n, max_n=max_n)
            answer = click.prompt(question.prompt, type=int)
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
    except Abort:
        scoreboard.print_summary(operations)
