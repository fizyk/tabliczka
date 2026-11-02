"""Tests for running the package as a program."""

import runpy
import sys
from unittest.mock import MagicMock

import click
import pytest


@pytest.mark.parametrize(
    ("frozen", "pauses"),
    [(True, ["Naciśnij dowolny klawisz, żeby zamknąć okno."]), (False, [])],
)
def test_main_module(
    monkeypatch: pytest.MonkeyPatch, *, frozen: bool, pauses: list[str]
) -> None:
    """The Windows program waits for a key before its window closes."""
    pause_mock = MagicMock(spec=click.pause)
    monkeypatch.setattr("click.pause", pause_mock)
    monkeypatch.setattr(sys, "frozen", frozen, raising=False)
    monkeypatch.setattr(sys, "argv", ["tabliczka", "--help"])

    with pytest.raises(SystemExit):
        runpy.run_module("tabliczka", run_name="__main__")

    assert [call.args[0] for call in pause_mock.call_args_list] == pauses
