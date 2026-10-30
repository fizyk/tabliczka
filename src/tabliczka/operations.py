"""Arithmetic operations and the questions they generate."""

from dataclasses import dataclass
from random import randint
from typing import Protocol


@dataclass(frozen=True)
class Question:
    """One exercise with its expected answer."""

    prompt: str
    answer: int
    operation_id: str


class Operation(Protocol):
    """An arithmetic skill that generates questions."""

    id: str
    heading: str

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        """Return a question with operands between ``min_n`` and ``max_n``."""
        ...


class Add:
    """Addition of two operands."""

    id = "add"
    heading = "Dodawanie:"

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        """Return an addition question."""
        x = randint(min_n, max_n)
        y = randint(min_n, max_n)
        return Question(f"Dodawanie: Ile to {x}+{y}?", x + y, self.id)


class Subtract:
    """Subtraction asked as ``(x+y)-x``, so the answer is the operand ``y``."""

    id = "subtract"
    heading = "Odejmowanie:"

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        """Return a subtraction question."""
        x = randint(min_n, max_n)
        y = randint(min_n, max_n)
        return Question(f"Odejmowanie: Ile to {x + y}-{x}?", y, self.id)


class Multiply:
    """Multiplication of two operands."""

    id = "multiplication"
    heading = "Mnożenie:"

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        """Return a multiplication question."""
        x = randint(min_n, max_n)
        y = randint(min_n, max_n)
        return Question(f"Mnożenie: Ile to {x}x{y}?", x * y, self.id)


class Divide:
    """Division asked as ``(x*y):x``, so the answer is the operand ``y``."""

    id = "division"
    heading = "Dzielenie:"

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        """Return a division question."""
        x = randint(min_n, max_n)
        y = randint(min_n, max_n)
        product = x * y
        return Question(f"Dzielenie: Ile to {product}:{x}?", y, self.id)


ADD = Add()
SUBTRACT = Subtract()
MULTIPLY = Multiply()
DIVIDE = Divide()
