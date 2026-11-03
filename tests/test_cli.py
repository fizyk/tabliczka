"""Tests for the command line."""

from typing import cast
from unittest.mock import MagicMock

import click
import pytest
from click.testing import CliRunner

from tabliczka.exercises.service import ADD
from tabliczka.practice.models import Score, Summary
from tabliczka.ui.cli import LEARNER_ANSWER, main, print_summary, run_drill

ADDITION_INTRO = "Nauczymy się dodawania i odejmowania!\n"
MULTIPLICATION_INTRO = "Nauczymy się tabliczki mnożenia i dzielenia!\n"
CHOSEN_INTRO = "Ćwiczymy wybrane działania!\n"
NAME_PROMPT = "Jak masz na imię?: "
DRILL_PROMPT = "Co ćwiczymy? (dodawanie, mnozenie, cwiczenie): "


@pytest.mark.parametrize(
    ("arguments", "typed", "output", "operation_ids", "max_n", "question_count"),
    [
        (
            ["--imie", "Ala", "dodawanie"],
            "",
            f"Witaj Ala!\n{ADDITION_INTRO}",
            ["add", "subtract"],
            None,
            None,
        ),
        (
            ["--imie", "Ala", "mnozenie", "--max", "12", "--pytania", "20"],
            "",
            f"Witaj Ala!\n{MULTIPLICATION_INTRO}",
            ["multiplication", "division"],
            12,
            20,
        ),
        (
            ["dodawanie", "--max", "30"],
            "Ala\n",
            f"{NAME_PROMPT}Ala\nWitaj Ala!\n{ADDITION_INTRO}",
            ["add", "subtract"],
            30,
            None,
        ),
        (
            ["--imie", "Ala"],
            "mnozenie\n",
            f"Witaj Ala!\n{DRILL_PROMPT}mnozenie\n{MULTIPLICATION_INTRO}",
            ["multiplication", "division"],
            None,
            None,
        ),
        (
            [],
            "Ala\ndodawanie\n",
            f"{NAME_PROMPT}Ala\nWitaj Ala!\n{DRILL_PROMPT}dodawanie\n{ADDITION_INTRO}",
            ["add", "subtract"],
            None,
            None,
        ),
        (
            ["--imie", "Ala"],
            "cwiczenie\n",
            f"Witaj Ala!\n{DRILL_PROMPT}cwiczenie\n{CHOSEN_INTRO}",
            ["add", "subtract", "multiplication", "division"],
            None,
            None,
        ),
        (
            [
                "--imie",
                "Ala",
                "cwiczenie",
                "--dzialanie",
                "dzielenie",
                "--dzialanie",
                "dodawanie",
                "--max",
                "50",
                "--pytania",
                "5",
            ],
            "",
            f"Witaj Ala!\n{CHOSEN_INTRO}",
            ["division", "add"],
            50,
            5,
        ),
    ],
)
def test_main(
    monkeypatch: pytest.MonkeyPatch,
    arguments: list[str],
    typed: str,
    output: str,
    operation_ids: list[str],
    max_n: int | None,
    question_count: int | None,
) -> None:
    """The learner is greeted and the drill starts, asking for what was not given."""
    # Given
    run_drill_mock = MagicMock(spec=run_drill)
    monkeypatch.setattr("tabliczka.ui.cli.run_drill", run_drill_mock)

    # When
    result = CliRunner().invoke(cast(click.Command, main), arguments, input=typed)

    # Then
    assert result.exit_code == 0
    assert result.output == output
    run_drill_mock.assert_called_once_with(
        operation_ids, max_n=max_n, question_count=question_count
    )


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (
            ["cwiczenie", "--dzialanie", "dodawanie", "--dzialanie", "dodawanie"],
            "Każde działanie wybierz tylko raz.",
        ),
        (["cwiczenie", "--dzialanie", "potegowanie"], "--dzialanie"),
        (["dodawanie", "--max", "1"], "--max"),
        (["mnozenie", "--pytania", "0"], "--pytania"),
    ],
)
def test_main__rejects(
    monkeypatch: pytest.MonkeyPatch, arguments: list[str], message: str
) -> None:
    """Options that cannot make a drill are rejected before it starts."""
    # Given
    run_drill_mock = MagicMock(spec=run_drill)
    monkeypatch.setattr("tabliczka.ui.cli.run_drill", run_drill_mock)

    # When
    result = CliRunner().invoke(
        cast(click.Command, main), ["--imie", "Ala", *arguments]
    )

    # Then
    assert result.exit_code == 2
    assert message in result.output
    run_drill_mock.assert_not_called()


def test_print_summary() -> None:
    """The summary prints the totals, then each operation's own score."""
    # Given
    summary = Summary(
        total=Score(correct=2, wrong=1),
        scores={"add": Score(correct=2), "subtract": Score(wrong=1)},
    )
    command = click.Command("summary", callback=lambda: print_summary(summary))

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
    summary = Summary(total=Score(), scores={"add": Score(), "subtract": Score()})
    command = click.Command("summary", callback=lambda: print_summary(summary))

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
    drill = click.Command("drill", callback=lambda: run_drill(["add"]))

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
    drill = click.Command(
        "drill", callback=lambda: run_drill(["add"], question_count=2)
    )

    # When
    result = CliRunner().invoke(drill, input="2\n2\n2\n")

    # Then
    assert result.exit_code == 0
    assert result.output.count("Ile to") == 2
    assert result.output.endswith("Dodawanie:\n2 - dobrze\n")


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
