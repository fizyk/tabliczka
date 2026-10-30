import click

from tabliczka.operations import ADD, DIVIDE, MULTIPLY, SUBTRACT
from tabliczka.session import run_drill


@click.group()
@click.argument("name", type=str, required=True)
def main(name: str) -> None:
    click.echo(f"Witaj {name}!")


@main.command()
def dodawanie() -> None:
    click.echo("Nauczymy się dodawania i odejmowania!")
    run_drill([ADD, SUBTRACT])


@main.command()
def mnozenie() -> None:
    click.echo("Nauczymy się tabliczki mnożenia i dzielenia!")
    run_drill([MULTIPLY, DIVIDE])