"""Tests for the drill session and scoreboard."""

from unittest.mock import MagicMock

import click
import pytest
from click.testing import CliRunner

from tabliczka.exercises.service import ADD, DIVIDE, MULTIPLY, SUBTRACT
from tabliczka.practice import api
from tabliczka.practice.models import Score, Scoreboard
from tabliczka.practice.service import LEARNER_ANSWER, print_summary, run_drill


def test_scoreboard() -> None:
    """The scoreboard counts each operation's answers and sums them."""
    # Given
    scoreboard = Scoreboard()

    # When
    scoreboard.record("add", correct=True)
    scoreboard.record("add", correct=False)
    scoreboard.record("subtract", correct=False)

    # Then
    assert scoreboard.score("add") == Score(correct=1, wrong=1)
    assert scoreboard.score("division") == Score()
    assert scoreboard.total(["add", "subtract"]) == Score(correct=1, wrong=2)


def test_print_summary() -> None:
    """The summary prints the totals, then each operation's own score."""
    # Given
    scoreboard = Scoreboard()
    scoreboard.record("add", correct=True)
    scoreboard.record("add", correct=True)
    scoreboard.record("subtract", correct=False)
    command = click.Command(
        "summary", callback=lambda: print_summary(scoreboard, [ADD, SUBTRACT])
    )

    # When
    result = CliRunner().invoke(command)

    # Then
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
        "====================\n"
        "Odejmowanie:\n"
        "0 - dobrze\n"
        "1 - źle\n"
    )


def test_print_summary__no_answers() -> None:
    """A drill with no answers prints no wrong answer lines."""
    # Given
    command = click.Command(
        "summary", callback=lambda: print_summary(Scoreboard(), [ADD, SUBTRACT])
    )

    # When
    result = CliRunner().invoke(command)

    # Then
    assert result.exit_code == 0
    assert "0 - dobrze" in result.output
    assert "źle" not in result.output


@pytest.mark.parametrize("typed", ["4\nkoniec\n", "4\n Koniec \n", "4\n"])
def test_run_drill(monkeypatch: pytest.MonkeyPatch, typed: str) -> None:
    """The drill scores each answer and prints the summary when the learner stops."""
    # Given
    monkeypatch.setattr("tabliczka.practice.service.choice", lambda operations: ADD)
    monkeypatch.setattr("tabliczka.exercises.service.randint", lambda low, high: low)
    drill = click.Command("drill", callback=lambda: run_drill([ADD]))

    # When
    result = CliRunner().invoke(drill, input=typed)

    # Then
    assert result.exit_code == 0
    assert result.output.startswith(
        "Wpisz „koniec”, żeby zakończyć.\nDodawanie: Ile to 1+1?: 4\n"
        "Niestety, źle, prawidłowy wynik to 2.\n"
    )
    assert "1 - źle" in result.output


def test_run_drill__stops_after_question_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The drill prints the summary once it has asked ``question_count`` questions."""
    # Given
    monkeypatch.setattr("tabliczka.practice.service.choice", lambda operations: ADD)
    monkeypatch.setattr("tabliczka.exercises.service.randint", lambda low, high: low)
    drill = click.Command("drill", callback=lambda: run_drill([ADD], question_count=2))

    # When
    result = CliRunner().invoke(drill, input="2\n2\n2\n")

    # Then
    assert result.exit_code == 0
    assert result.output.count("Ile to") == 2
    assert result.output.endswith("Dodawanie:\n2 - dobrze\n")


@pytest.mark.parametrize(
    ("max_n", "upper_bounds"),
    [(None, [20, 10]), (7, [7, 7])],
)
def test_run_drill__max_n(
    monkeypatch: pytest.MonkeyPatch, max_n: int | None, upper_bounds: list[int]
) -> None:
    """Each operation uses ``max_n`` when given and its own default otherwise."""
    # Given
    operations = iter((ADD, MULTIPLY))
    monkeypatch.setattr(
        "tabliczka.practice.service.choice", lambda choices: next(operations)
    )
    asked_upper_bounds: list[int] = []

    def randint(low: int, high: int) -> int:
        asked_upper_bounds.append(high)
        return low

    monkeypatch.setattr("tabliczka.exercises.service.randint", randint)
    drill = click.Command(
        "drill",
        callback=lambda: run_drill([ADD, MULTIPLY], max_n=max_n, question_count=2),
    )

    # When
    result = CliRunner().invoke(drill, input="2\n4\n")

    # Then
    assert result.exit_code == 0
    assert [asked_upper_bounds[0], asked_upper_bounds[2]] == upper_bounds


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


def test_api_run_drill(monkeypatch: pytest.MonkeyPatch) -> None:
    """The drill runs the operations whose ids it is given."""
    # Given
    run_drill_mock = MagicMock(spec=run_drill)
    monkeypatch.setattr("tabliczka.practice.service.run_drill", run_drill_mock)

    # When
    api.run_drill(["division", "add"], max_n=12, question_count=5)

    # Then
    run_drill_mock.assert_called_once_with([DIVIDE, ADD], max_n=12, question_count=5)
