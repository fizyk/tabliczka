"""Tests for running the package as a program."""

import runpy
from unittest.mock import MagicMock

import pytest

from tabliczka.ui import window


def test_main_module(monkeypatch: pytest.MonkeyPatch) -> None:
    """The package opens the window when run as a program."""
    # Given
    main_mock = MagicMock(spec=window.main)
    monkeypatch.setattr(window, "main", main_mock)

    # When
    runpy.run_module("tabliczka", run_name="__main__")

    # Then
    main_mock.assert_called_once_with()
