"""Polish copy shared by the command line and the window."""

from tabliczka.exercises.models import Question
from tabliczka.practice.models import Score

OPERATION_HEADINGS_BY_ID = {
    "add": "Dodawanie",
    "subtract": "Odejmowanie",
    "multiplication": "Mnożenie",
    "division": "Dzielenie",
    "division_with_remainder": "Dzielenie z resztą",
    "square": "Kwadraty",
    "cube": "Sześciany",
}

CORRECT_FEEDBACK = "Dobrze!"
REMAINDER_WORD = "reszty"
SUMMARY_HEADING = "Twój wynik to:"


def greeting(name: str) -> str:
    """Return the welcome for the learner."""
    return f"Witaj {name}!"


def question_text(question: Question) -> str:
    """Return the question as asked: the operation's heading and the expression."""
    heading = OPERATION_HEADINGS_BY_ID[question.operation_id]
    return f"{heading}: Ile to {question.expression}?"


def answer_text(question: Question) -> str:
    """Return the correct answer as said aloud, with the remainder when it has one."""
    if question.remainder is None:
        return str(question.answer)
    return f"{question.answer} {REMAINDER_WORD} {question.remainder}"


def wrong_feedback(question: Question) -> str:
    """Return the feedback on a wrong answer, with the correct one."""
    return f"Niestety, źle, prawidłowy wynik to {answer_text(question)}."


def correct_count(score: Score) -> str:
    """Return the line with the number of correct answers."""
    return f"{score.correct} - dobrze"


def wrong_count(score: Score) -> str:
    """Return the line with the number of wrong answers."""
    return f"{score.wrong} - źle"
