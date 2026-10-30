"""Tests for the arithmetic operations."""

import re

import pytest

from tabliczka.operations import ADD, DIVIDE, MULTIPLY, SUBTRACT, Operation


@pytest.mark.parametrize(
    ("operation", "expected_prompt", "expected_answer", "expected_id"),
    [
        (ADD, "Dodawanie: Ile to 4+2?", 6, "add"),
        (SUBTRACT, "Odejmowanie: Ile to 6-4?", 2, "subtract"),
        (MULTIPLY, "Mnożenie: Ile to 4x2?", 8, "multiplication"),
        (DIVIDE, "Dzielenie: Ile to 8:4?", 2, "division"),
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
    operands = iter((4, 2))
    monkeypatch.setattr(
        "tabliczka.operations.randint", lambda min_n, max_n: next(operands)
    )

    question = operation.generate()

    assert question.prompt == expected_prompt
    assert question.answer == expected_answer
    assert question.operation_id == expected_id


@pytest.mark.parametrize("operation", [ADD, SUBTRACT, MULTIPLY, DIVIDE])
def test_generate_respects_operand_bounds(operation: Operation) -> None:
    """Generated operands stay within the requested range."""
    for _ in range(100):
        question = operation.generate(max_n=5)
        numbers = [
            int(number)
            for number in re.findall(r"\d+", question.prompt.split("Ile to ", 1)[1])
        ]

        if operation is ADD or operation is MULTIPLY:
            operands = numbers
        elif operation is SUBTRACT:
            minuend, x = numbers
            operands = [x, question.answer]
            assert minuend == x + question.answer
        else:
            product, x = numbers
            operands = [x, question.answer]
            assert product == x * question.answer

        assert all(1 <= operand <= 5 for operand in operands)
