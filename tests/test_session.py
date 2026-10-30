import click
from click.testing import CliRunner

from tabliczka.operations import ADD, SUBTRACT
from tabliczka.session import Scoreboard, run_drill


def test_summary_prints_totals_and_per_operation_scores() -> None:
    scoreboard = Scoreboard()
    scoreboard.record("add", correct=True)
    scoreboard.record("add", correct=True)
    scoreboard.record("subtract", correct=False)

    @click.command()
    def command() -> None:
        scoreboard.print_summary([ADD, SUBTRACT])

    result = CliRunner().invoke(command)

    assert result.exit_code == 0
    assert result.output == (
        "\n\n"
        "====================\n"
        "Twój wynik to:\n"
        "2 - dobrze\n"
        "1 - źle\n"
        "====================\n"
        "Dodawanie:\n"
        "2 - dobrze\n"
        "0 - źle\n"
        "====================\n"
        "Odejmowanie:\n"
        "0 - dobrze\n"
        "1 - źle\n"
    )


def test_empty_summary_has_no_wrong_answer_lines() -> None:
    scoreboard = Scoreboard()

    @click.command()
    def command() -> None:
        scoreboard.print_summary([ADD, SUBTRACT])

    result = CliRunner().invoke(command)

    assert result.exit_code == 0
    assert "0 - dobrze" in result.output
    assert "źle" not in result.output


def test_run_drill_records_answers_and_summarizes_on_abort(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr("tabliczka.session.choice", lambda operations: ADD)
    monkeypatch.setattr("tabliczka.operations.randint", lambda min_n, max_n: 2)
    prompts = []

    def prompt(text: str, **kwargs: object) -> int:
        prompts.append((text, kwargs["type"]))
        if len(prompts) == 1:
            return 4
        raise click.Abort()

    monkeypatch.setattr("tabliczka.session.click.prompt", prompt)

    run_drill([ADD], max_n=5)

    output = capsys.readouterr().out
    assert prompts == [("Dodawanie: Ile to 2+2?", int)] * 2
    assert "Dobrze!" in output
    assert "1 - dobrze" in output