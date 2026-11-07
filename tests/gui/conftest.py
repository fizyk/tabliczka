"""Fixtures shared by the tests of the window."""

import pytest

from tabliczka.exercises.service import ADD


@pytest.fixture
def addition_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make every question ``1+1``."""
    monkeypatch.setattr("tabliczka.practice.service.choice", lambda operations: ADD)
    monkeypatch.setattr("tabliczka.exercises.service.randint", lambda low, high: low)
