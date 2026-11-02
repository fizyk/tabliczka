"""Command line for the arithmetic drills."""

from collections.abc import Callable, Sequence

import click

from tabliczka.practice.api import run_drill

OPERATION_IDS_BY_NAME = {
    "dodawanie": "add",
    "odejmowanie": "subtract",
    "mnozenie": "multiplication",
    "dzielenie": "division",
}


def drill_options[CommandFunction: Callable[..., None]](
    command: CommandFunction,
) -> CommandFunction:
    """Add the largest number and the number of questions to a drill command."""
    command = click.option(
        "--max",
        "max_n",
        type=click.IntRange(min=2),
        help="Ustala największą liczbę w pytaniach (sumę, odjemną albo czynnik); "
        "domyślnie 20 przy dodawaniu i odejmowaniu, 10 przy mnożeniu i dzieleniu.",
    )(command)
    return click.option(
        "--pytania",
        "question_count",
        type=click.IntRange(min=1),
        help="Ustala, ile pytań padnie przed wynikiem; bez tej opcji ćwiczenie "
        "trwa do wpisania „koniec”.",
    )(command)


def chosen_operation_ids(
    context: click.Context, parameter: click.Parameter, names: tuple[str, ...]
) -> list[str]:
    """Return the ids of the chosen operations, rejecting one chosen twice."""
    if len(set(names)) != len(names):
        raise click.BadParameter("Każde działanie wybierz tylko raz.")
    return [OPERATION_IDS_BY_NAME[name] for name in names]


@click.group(
    invoke_without_command=True,
    help="Wita ucznia i uruchamia ćwiczenie. O brakujące imię lub ćwiczenie "
    "program zapyta.",
)
@click.option(
    "--imie",
    "name",
    prompt="Jak masz na imię?",
    help="Imię ucznia do powitania. Jeśli go brak, program o nie zapyta.",
)
@click.pass_context
def main(context: click.Context, name: str) -> None:
    """Greet the learner by name, then run the drill, asking which when missing."""
    click.echo(f"Witaj {name}!")
    if context.invoked_subcommand is None:
        drill = click.prompt("Co ćwiczymy?", type=click.Choice(list(main.commands)))
        context.invoke(main.commands[drill])


@main.command(help="Ćwiczy dodawanie i odejmowanie.")
@drill_options
def dodawanie(max_n: int | None, question_count: int | None) -> None:
    """Drill addition and subtraction."""
    click.echo("Nauczymy się dodawania i odejmowania!")
    run_drill(["add", "subtract"], max_n=max_n, question_count=question_count)


@main.command(help="Ćwiczy mnożenie i dzielenie.")
@drill_options
def mnozenie(max_n: int | None, question_count: int | None) -> None:
    """Drill multiplication and division."""
    click.echo("Nauczymy się tabliczki mnożenia i dzielenia!")
    run_drill(
        ["multiplication", "division"], max_n=max_n, question_count=question_count
    )


@main.command(help="Ćwiczy wybrane działania, domyślnie wszystkie cztery.")
@click.option(
    "--dzialanie",
    "operation_ids",
    type=click.Choice(list(OPERATION_IDS_BY_NAME)),
    multiple=True,
    callback=chosen_operation_ids,
    help="Wybiera działanie do ćwiczenia; podaj kilka razy, żeby ćwiczyć kilka, "
    "a bez tej opcji program ćwiczy wszystkie cztery.",
)
@drill_options
def cwiczenie(
    operation_ids: Sequence[str], max_n: int | None, question_count: int | None
) -> None:
    """Drill the chosen operations, all four when none is chosen."""
    click.echo("Ćwiczymy wybrane działania!")
    run_drill(
        operation_ids or list(OPERATION_IDS_BY_NAME.values()),
        max_n=max_n,
        question_count=question_count,
    )
