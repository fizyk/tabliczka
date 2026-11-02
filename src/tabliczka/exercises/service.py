"""The four arithmetic operations."""

from random import randint

from tabliczka.exercises.models import Operation, Question


class Add:
    """Addition of two operands whose sum is at most the largest number."""

    id = "add"
    heading = "Dodawanie:"
    default_max_n = 20

    def generate(self, max_n: int) -> Question:
        """Return an addition question."""
        answer = randint(2, max_n)
        x = randint(1, answer - 1)
        return Question(f"Dodawanie: Ile to {x}+{answer - x}?", answer, self.id)


class Subtract:
    """Subtraction asked as ``(x+y)-x``, with the minuend at most the largest number."""

    id = "subtract"
    heading = "Odejmowanie:"
    default_max_n = 20

    def generate(self, max_n: int) -> Question:
        """Return a subtraction question."""
        minuend = randint(2, max_n)
        x = randint(1, minuend - 1)
        return Question(f"Odejmowanie: Ile to {minuend}-{x}?", minuend - x, self.id)


class Multiply:
    """Multiplication of two factors, each at most the largest number."""

    id = "multiplication"
    heading = "Mnożenie:"
    default_max_n = 10

    def generate(self, max_n: int) -> Question:
        """Return a multiplication question."""
        x = randint(1, max_n)
        y = randint(1, max_n)
        return Question(f"Mnożenie: Ile to {x}x{y}?", x * y, self.id)


class Divide:
    """Division ``(x*y):x``, with ``x`` and ``y`` at most the largest number."""

    id = "division"
    heading = "Dzielenie:"
    default_max_n = 10

    def generate(self, max_n: int) -> Question:
        """Return a division question."""
        x = randint(1, max_n)
        y = randint(1, max_n)
        product = x * y
        return Question(f"Dzielenie: Ile to {product}:{x}?", y, self.id)


ADD = Add()
SUBTRACT = Subtract()
MULTIPLY = Multiply()
DIVIDE = Divide()

OPERATIONS_BY_ID: dict[str, Operation] = {
    operation.id: operation for operation in (ADD, SUBTRACT, MULTIPLY, DIVIDE)
}
