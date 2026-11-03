"""Command line for the arithmetic drills."""

from collections.abc import Callable, Sequence
from contextlib import suppress

import click
from click import Abort

from tabliczka.practice.api import ask_questions, check_answer, start_drill
from tabliczka.practice.models import Drill, Score

STOP_WORD = "koniec"

OPERATION_IDS_BY_NAME = {
    "dodawanie": "add",
    "odejmowanie": "subtract",
    "mnozenie": "multiplication",
    "dzielenie": "division",
}


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


def print_summary(drill: Drill) -> None:
    """Print the totals, then the score of each operation."""
    click.echo("\n")
    click.echo("=" * 20)
    click.echo("Twój wynik to:")
    print_score(drill.scoreboard.total(operation.id for operation in drill.operations))
    click.echo("=" * 20)

    for index, operation in enumerate(drill.operations):
        if index:
            click.echo("=" * 20)
        click.echo(operation.heading)
        print_score(drill.scoreboard.score(operation.id))


def run_drill(
    operation_ids: Sequence[str],
    *,
    max_n: int | None = None,
    question_count: int | None = None,
) -> None:
    """Ask questions until the learner stops, aborts or answers ``question_count``.

    Then print the summary.
    """
    drill = start_drill(operation_ids, max_n=max_n, question_count=question_count)
    click.echo(f"Wpisz „{STOP_WORD}”, żeby zakończyć.")
    with suppress(Abort):
        for question in ask_questions(drill):
            given = click.prompt(question.prompt, type=LEARNER_ANSWER)
            if given is None:
                break
            if check_answer(drill, question, given):
                click.echo(click.style("Dobrze!", fg="green"))
            else:
                click.echo(
                    click.style(
                        f"Niestety, źle, prawidłowy wynik to {question.answer}.",
                        fg="red",
                    )
                )
    print_summary(drill)


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
