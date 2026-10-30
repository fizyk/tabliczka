"""Command line for the arithmetic drills."""

import click

from tabliczka.operations import ADD, DIVIDE, MULTIPLY, SUBTRACT
from tabliczka.session import run_drill


@click.group()
@click.argument("name", type=str, required=True)
def main(name: str) -> None:
    """Greet the learner by name."""
    click.echo(f"Witaj {name}!")


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
