"""Tests for the command line."""

from typing import cast

import click
import pytest
from click.testing import CliRunner

from tabliczka.cli import main
from tabliczka.operations import ADD, DIVIDE, MULTIPLY, SUBTRACT, Operation

ADDITION_INTRO = "Nauczymy się dodawania i odejmowania!\n"
MULTIPLICATION_INTRO = "Nauczymy się tabliczki mnożenia i dzielenia!\n"
NAME_PROMPT = "Jak masz na imię?: "
DRILL_PROMPT = "Co ćwiczymy? (dodawanie, mnozenie): "


@pytest.mark.parametrize(
    ("arguments", "typed", "output", "operations"),
    [
        (
            ["--imie", "Ala", "dodawanie"],
            "",
            f"Witaj Ala!\n{ADDITION_INTRO}",
            [ADD, SUBTRACT],
        ),
        (
            ["--imie", "Ala", "mnozenie"],
            "",
            f"Witaj Ala!\n{MULTIPLICATION_INTRO}",
            [MULTIPLY, DIVIDE],
        ),
        (
            ["dodawanie"],
            "Ala\n",
            f"{NAME_PROMPT}Ala\nWitaj Ala!\n{ADDITION_INTRO}",
            [ADD, SUBTRACT],
        ),
        (
            ["--imie", "Ala"],
            "mnozenie\n",
            f"Witaj Ala!\n{DRILL_PROMPT}mnozenie\n{MULTIPLICATION_INTRO}",
            [MULTIPLY, DIVIDE],
        ),
        (
            [],
            "Ala\ndodawanie\n",
            f"{NAME_PROMPT}Ala\nWitaj Ala!\n{DRILL_PROMPT}dodawanie\n{ADDITION_INTRO}",
            [ADD, SUBTRACT],
        ),
    ],
)
def test_main(
    monkeypatch: pytest.MonkeyPatch,
    arguments: list[str],
    typed: str,
    output: str,
    operations: list[Operation],
) -> None:
    """The learner is greeted and the drill starts, asking for what was not given."""
    calls: list[list[Operation]] = []
    monkeypatch.setattr(
        "tabliczka.cli.run_drill", lambda selected: calls.append(selected)
    )

    result = CliRunner().invoke(cast(click.Command, main), arguments, input=typed)

    assert result.exit_code == 0
    assert result.output == output
    assert calls == [operations]
