"""Tests for the drill session and scoreboard."""

import click
import pytest
from click.testing import CliRunner

from tabliczka.operations import ADD, SUBTRACT
from tabliczka.session import LEARNER_ANSWER, Scoreboard, run_drill


def test_summary_prints_totals_and_per_operation_scores() -> None:
    """The summary prints the totals, then each operation's score."""
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
    """A drill with no answers prints no wrong answer lines."""
    scoreboard = Scoreboard()

    @click.command()
    def command() -> None:
        scoreboard.print_summary([ADD, SUBTRACT])

    result = CliRunner().invoke(command)

    assert result.exit_code == 0
    assert "0 - dobrze" in result.output
    assert "źle" not in result.output


@pytest.mark.parametrize("typed", ["4\nkoniec\n", "4\n Koniec \n", "4\n"])
def test_run_drill__prints_summary(monkeypatch: pytest.MonkeyPatch, typed: str) -> None:
    """The drill scores each answer and prints the summary when the learner stops."""
    monkeypatch.setattr("tabliczka.session.choice", lambda operations: ADD)
    monkeypatch.setattr("tabliczka.operations.randint", lambda min_n, max_n: 2)
    drill = click.Command("drill", callback=lambda: run_drill([ADD], max_n=5))

    result = CliRunner().invoke(drill, input=typed)

    assert result.exit_code == 0
    assert result.output.startswith(
        "Wpisz „koniec”, żeby zakończyć.\nDodawanie: Ile to 2+2?: 4\nDobrze!\n"
    )
    assert "1 - dobrze" in result.output


@pytest.mark.parametrize(
    ("typed", "answer"),
    [("4", 4), (" 12 ", 12), ("koniec", None), (" KONIEC ", None)],
)
def test_learner_answer(typed: str, answer: int | None) -> None:
    """A typed whole number is the answer; the stop word ends the drill."""
    assert LEARNER_ANSWER.convert(typed, None, None) == answer


@pytest.mark.parametrize("typed", ["", "cztery", "4.5"])
def test_learner_answer__rejects(typed: str) -> None:
    """Anything but a whole number or the stop word is asked for again."""
    with pytest.raises(click.BadParameter, match="Wpisz liczbę albo „koniec”."):
        LEARNER_ANSWER.convert(typed, None, None)
