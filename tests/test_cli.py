"""Tests for the command line."""

from typing import cast
from unittest.mock import MagicMock

import click
import pytest
from click.testing import CliRunner

from tabliczka.practice.api import run_drill
from tabliczka.ui.cli import main

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
