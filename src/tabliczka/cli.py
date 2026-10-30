"""Command line for the arithmetic drills."""

import click

from tabliczka.operations import ADD, DIVIDE, MULTIPLY, SUBTRACT
from tabliczka.session import run_drill


@click.group(invoke_without_command=True)
@click.option(
    "--imie",
    "name",
    prompt="Jak masz na imię?",
    help="Name to greet the learner by. Asked for when missing.",
)
@click.pass_context
def main(context: click.Context, name: str) -> None:
    """Greet the learner by name, then run the drill, asking which when missing."""
    click.echo(f"Witaj {name}!")
    if context.invoked_subcommand is None:
        drill = click.prompt("Co ćwiczymy?", type=click.Choice(list(main.commands)))
        context.invoke(main.commands[drill])


@main.command()
def dodawanie() -> None:
    """Drill addition and subtraction."""
    click.echo("Nauczymy się dodawania i odejmowania!")
    run_drill([ADD, SUBTRACT])


@main.command()
def mnozenie() -> None:
    """Drill multiplication and division."""
    click.echo("Nauczymy się tabliczki mnożenia i dzielenia!")
    run_drill([MULTIPLY, DIVIDE])
