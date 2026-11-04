"""The four arithmetic operations, and finding them by id."""

from collections import Counter
from collections.abc import Sequence
from random import randint

from tabliczka.exercises.models import Operation, Question


class Add:
    """Addition of two operands whose sum is at most the largest number."""

    id = "add"
    default_max_n = 20
    min_max_n = 2

    def generate(self, max_n: int) -> Question:
        """Return an addition question."""
        answer = randint(2, max_n)
        x = randint(1, answer - 1)
        return Question(f"{x}+{answer - x}", answer, self.id)


class Subtract:
    """Subtraction asked as ``(x+y)-x``, with the minuend at most the largest number."""

    id = "subtract"
    default_max_n = 20
    min_max_n = 2

    def generate(self, max_n: int) -> Question:
        """Return a subtraction question."""
        minuend = randint(2, max_n)
        x = randint(1, minuend - 1)
        return Question(f"{minuend}-{x}", minuend - x, self.id)


class Multiply:
    """Multiplication of two factors, each at most the largest number."""

    id = "multiplication"
    default_max_n = 10
    min_max_n = 1

    def generate(self, max_n: int) -> Question:
        """Return a multiplication question."""
        x = randint(1, max_n)
        y = randint(1, max_n)
        return Question(f"{x}x{y}", x * y, self.id)


class Divide:
    """Division ``(x*y):x``, with ``x`` and ``y`` at most the largest number."""

    id = "division"
    default_max_n = 10
    min_max_n = 1

    def generate(self, max_n: int) -> Question:
        """Return a division question."""
        x = randint(1, max_n)
        y = randint(1, max_n)
        product = x * y
        return Question(f"{product}:{x}", y, self.id)


ADD = Add()
SUBTRACT = Subtract()
MULTIPLY = Multiply()
DIVIDE = Divide()

OPERATIONS_BY_ID: dict[str, Operation] = {
    operation.id: operation for operation in (ADD, SUBTRACT, MULTIPLY, DIVIDE)
}


def get_operations(operation_ids: Sequence[str]) -> list[Operation]:
    """Return the operations with the given ids, in the same order.

    Reject ids no operation has, and ids given more than once.
    """
    unknown = set(operation_ids) - OPERATIONS_BY_ID.keys()
    if unknown:
        raise ValueError(
            f"Unknown operation ids {sorted(unknown)}. "
            f"Use ids from {list(OPERATIONS_BY_ID)}."
        )
    repeated = [
        operation_id
        for operation_id, uses in Counter(operation_ids).items()
        if uses > 1
    ]
    if repeated:
        raise ValueError(f"Operation ids {repeated} are repeated. Give each id once.")
    return [OPERATIONS_BY_ID[operation_id] for operation_id in operation_ids]
