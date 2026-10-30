from typing import cast

import click
import pytest
from click.testing import CliRunner

from tabliczka.cli import main
from tabliczka.operations import ADD, DIVIDE, MULTIPLY, SUBTRACT, Operation


@pytest.mark.parametrize(
    ("command", "intro", "operations"),
    [
        (
            "dodawanie",
            "Nauczymy się dodawania i odejmowania!",
            [ADD, SUBTRACT],
        ),
        (
            "mnozenie",
            "Nauczymy się tabliczki mnożenia i dzielenia!",
            [MULTIPLY, DIVIDE],
        ),
    ],
)
def test_commands_greet_and_start_the_expected_drill(
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    intro: str,
    operations: list[Operation],
) -> None:
    calls: list[list[Operation]] = []
    monkeypatch.setattr("tabliczka.cli.run_drill", lambda selected: calls.append(selected))

    result = CliRunner().invoke(cast(click.Command, main), ["Ala", command])

    assert result.exit_code == 0
    assert result.output == f"Witaj Ala!\n{intro}\n"
    assert calls == [operations]