from dataclasses import dataclass
from random import randint
from typing import Protocol


@dataclass(frozen=True)
class Question:
    prompt: str
    answer: int
    operation_id: str


class Operation(Protocol):
    id: str
    heading: str

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question: ...


class Add:
    id = "add"
    heading = "Dodawanie:"

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        x = randint(min_n, max_n)
        y = randint(min_n, max_n)
        return Question(f"Dodawanie: Ile to {x}+{y}?", x + y, self.id)


class Subtract:
    id = "subtract"
    heading = "Odejmowanie:"

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        x = randint(min_n, max_n)
        y = randint(min_n, max_n)
        return Question(f"Odejmowanie: Ile to {x + y}-{x}?", y, self.id)


class Multiply:
    id = "multiplication"
    heading = "Mnożenie:"

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        x = randint(min_n, max_n)
        y = randint(min_n, max_n)
        return Question(f"Mnożenie: Ile to {x}x{y}?", x * y, self.id)


class Divide:
    id = "division"
    heading = "Dzielenie:"

    def generate(self, min_n: int = 1, max_n: int = 10) -> Question:
        x = randint(min_n, max_n)
        y = randint(min_n, max_n)
        product = x * y
        return Question(f"Dzielenie: Ile to {product}:{x}?", y, self.id)


ADD = Add()
SUBTRACT = Subtract()
MULTIPLY = Multiply()
DIVIDE = Divide()