"""Tests for the arithmetic operations."""

import re

import pytest

from tabliczka.exercises.api import get_operations
from tabliczka.exercises.models import Operation
from tabliczka.exercises.service import ADD, DIVIDE, MULTIPLY, SUBTRACT


@pytest.mark.parametrize(
    ("operation", "expected_prompt", "expected_answer", "expected_id"),
    [
        (ADD, "Dodawanie: Ile to 2+4?", 6, "add"),
        (SUBTRACT, "Odejmowanie: Ile to 6-2?", 4, "subtract"),
        (MULTIPLY, "Mnożenie: Ile to 6x2?", 12, "multiplication"),
        (DIVIDE, "Dzielenie: Ile to 12:6?", 2, "division"),
    ],
)
def test_generate_preserves_question_format(
    monkeypatch: pytest.MonkeyPatch,
    operation: Operation,
    expected_prompt: str,
    expected_answer: int,
    expected_id: str,
) -> None:
    """Generated questions keep their prompt, answer and operation id."""
    # Given
    numbers = iter((6, 2))
    monkeypatch.setattr(
        "tabliczka.exercises.service.randint", lambda low, high: next(numbers)
    )

    # When
    question = operation.generate(10)

    # Then
    assert question.prompt == expected_prompt
    assert question.answer == expected_answer
    assert question.operation_id == expected_id


@pytest.mark.parametrize(
    ("operation", "default_max_n"),
    [(ADD, 20), (SUBTRACT, 20), (MULTIPLY, 10), (DIVIDE, 10)],
)
def test_default_max_n(operation: Operation, default_max_n: int) -> None:
    """Addition and subtraction default to 20, multiplication and division to 10."""
    assert operation.default_max_n == default_max_n


def numbers_in(prompt: str) -> list[int]:
    """Return the numbers a question prompt asks about."""
    return [int(number) for number in re.findall(r"\d+", prompt.split("Ile to ")[1])]


@pytest.mark.parametrize("operation", [ADD, SUBTRACT])
@pytest.mark.parametrize("max_n", [2, 7])
def test_generate__sum_within_max_n(operation: Operation, max_n: int) -> None:
    """Addition and subtraction keep the sum of the operands within ``max_n``."""
    for _ in range(100):
        # When
        question = operation.generate(max_n)

        # Then
        first, second = numbers_in(question.prompt)
        if operation is ADD:
            assert first >= 1 and second >= 1
            assert question.answer == first + second <= max_n
        else:
            assert second >= 1 and question.answer >= 1
            assert first == second + question.answer <= max_n


@pytest.mark.parametrize("operation", [MULTIPLY, DIVIDE])
def test_generate__factors_within_max_n(operation: Operation) -> None:
    """Multiplication and division keep each factor within ``max_n``."""
    for _ in range(100):
        # When
        question = operation.generate(5)

        # Then
        first, second = numbers_in(question.prompt)
        if operation is MULTIPLY:
            factors = [first, second]
            assert question.answer == first * second
        else:
            factors = [second, question.answer]
            assert first == second * question.answer
        assert all(1 <= factor <= 5 for factor in factors)


def test_get_operations() -> None:
    """Operations come back in the order their ids were given."""
    assert get_operations(["division", "add"]) == [DIVIDE, ADD]


@pytest.mark.parametrize(
    ("operation_ids", "message"),
    [
        (["add", "power"], r"Unknown operation ids \['power'\]"),
        (["add", "division", "add"], r"Operation ids \['add'\] are repeated"),
    ],
)
def test_get_operations__rejects(operation_ids: list[str], message: str) -> None:
    """An id no operation has, or one given twice, is rejected."""
    with pytest.raises(ValueError, match=message):
        get_operations(operation_ids)
