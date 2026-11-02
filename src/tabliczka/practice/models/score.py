"""The result of one operation in a drill."""

from dataclasses import dataclass


@dataclass
class Score:
    """Correct and wrong answer counts."""

    correct: int = 0
    wrong: int = 0
