"""Tests for the arithmetic operations."""

import re

import pytest

from tabliczka.exercises import get_operations
from tabliczka.exercises.models import Operation
from tabliczka.exercises.service import (
    ADD,
    CUBE,
    DIVIDE,
    DIVIDE_WITH_REMAINDER,
    MULTIPLY,
    SQUARE,
    SUBTRACT,
)


@pytest.mark.parametrize(
    (
        "operation",
        "expected_expression",
        "expected_answer",
        "expected_remainder",
        "expected_id",
    ),
    [
        (ADD, "2+4", 6, None, "add"),
        (SUBTRACT, "6-2", 4, None, "subtract"),
        (MULTIPLY, "6x2", 12, None, "multiplication"),
        (DIVIDE, "12:6", 2, None, "division"),
        (DIVIDE_WITH_REMAINDER, "15:6", 2, 3, "division_with_remainder"),
        (SQUARE, "6²", 36, None, "square"),
        (CUBE, "6³", 216, None, "cube"),
    ],
)
def test_generate(
    monkeypatch: pytest.MonkeyPatch,
    operation: Operation,
    expected_expression: str,
    expected_answer: int,
    expected_remainder: int | None,
    expected_id: str,
) -> None:
    """Generated questions keep their expression, answer, remainder and operation id."""
    # Given
    numbers = iter((6, 2, 3))
    monkeypatch.setattr(
        "tabliczka.exercises.service.randint", lambda low, high: next(numbers)
    )

    # When
    question = operation.generate(10)

    # Then
    assert question.expression == expected_expression
    assert question.answer == expected_answer
    assert question.remainder == expected_remainder
    assert question.operation_id == expected_id


@pytest.mark.parametrize(
    ("operation", "default_largest_number"),
    [
        (ADD, 20),
        (SUBTRACT, 20),
        (MULTIPLY, 10),
        (DIVIDE, 10),
        (DIVIDE_WITH_REMAINDER, 10),
        (SQUARE, 10),
        (CUBE, 5),
    ],
)
def test_default_largest_number(
    operation: Operation, default_largest_number: int
) -> None:
    """Addition and subtraction default to 20, cubes to 5, the others to 10."""
    assert operation.default_largest_number == default_largest_number


@pytest.mark.parametrize(
    ("operation", "smallest_largest_number"),
    [
        (ADD, 2),
        (SUBTRACT, 2),
        (MULTIPLY, 1),
        (DIVIDE, 1),
        (DIVIDE_WITH_REMAINDER, 2),
        (SQUARE, 1),
        (CUBE, 1),
    ],
)
def test_generate__smallest_largest_number(
    operation: Operation, smallest_largest_number: int
) -> None:
    """Each operation can generate a question with its smallest largest number."""
    # When
    question = operation.generate(smallest_largest_number)

    # Then
    assert operation.smallest_largest_number == smallest_largest_number
    assert question.answer >= 1


def numbers_in(expression: str) -> list[int]:
    """Return the numbers a question's expression asks about."""
    return [int(number) for number in re.findall(r"\d+", expression)]


@pytest.mark.parametrize("operation", [ADD, SUBTRACT])
@pytest.mark.parametrize("largest_number", [2, 7])
def test_generate__sum_within_largest_number(
    operation: Operation, largest_number: int
) -> None:
    """Addition and subtraction keep the operands' sum within ``largest_number``."""
    for _ in range(100):
        # When
        question = operation.generate(largest_number)

        # Then
        first, second = numbers_in(question.expression)
        if operation is ADD:
            assert first >= 1 and second >= 1
            assert question.answer == first + second <= largest_number
        else:
            assert second >= 1 and question.answer >= 1
            assert first == second + question.answer <= largest_number


@pytest.mark.parametrize("operation", [MULTIPLY, DIVIDE])
def test_generate__factors_within_largest_number(operation: Operation) -> None:
    """Multiplication and division keep each factor within ``largest_number``."""
    for _ in range(100):
        # When
        question = operation.generate(5)

        # Then
        first, second = numbers_in(question.expression)
        if operation is MULTIPLY:
            factors = [first, second]
            assert question.answer == first * second
        else:
            factors = [second, question.answer]
            assert first == second * question.answer
        assert all(1 <= factor <= 5 for factor in factors)


def test_generate__remainder_below_divisor() -> None:
    """Division with remainder keeps the divisor and quotient within the limit.

    The remainder stays between 1 and one below the divisor.
    """
    for _ in range(100):
        # When
        question = DIVIDE_WITH_REMAINDER.generate(5)

        # Then
        dividend, divisor = numbers_in(question.expression)
        assert question.remainder is not None
        assert dividend == divisor * question.answer + question.remainder
        assert 2 <= divisor <= 5
        assert 1 <= question.answer <= 5
        assert 1 <= question.remainder < divisor


@pytest.mark.parametrize(("operation", "power"), [(SQUARE, 2), (CUBE, 3)])
def test_generate__base_within_largest_number(operation: Operation, power: int) -> None:
    """Squares and cubes keep the base within ``largest_number``."""
    for _ in range(100):
        # When
        question = operation.generate(5)

        # Then
        [base] = numbers_in(question.expression)
        assert 1 <= base <= 5
        assert question.answer == base**power


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
