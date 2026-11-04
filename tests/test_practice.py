"""Tests for drills and their scores."""

import pytest

from tabliczka.exercises.service import ADD, DIVIDE, MULTIPLY
from tabliczka.practice.api import Drill
from tabliczka.practice.models import Score, Scoreboard, Summary


def test_scoreboard() -> None:
    """The scoreboard counts each operation's answers."""
    # Given
    scoreboard = Scoreboard()

    # When
    scoreboard.record("add", correct=True)
    scoreboard.record("add", correct=False)
    scoreboard.record("subtract", correct=False)

    # Then
    assert scoreboard.score("add") == Score(correct=1, wrong=1)
    assert scoreboard.score("division") == Score()


def test_drill() -> None:
    """A drill starts with the operations whose ids it is given and no answers."""
    # When
    drill = Drill(["division", "add"], max_n=12, question_count=5)

    # Then
    assert drill.operations == [DIVIDE, ADD]
    assert (drill.max_n, drill.question_count) == (12, 5)
    assert drill.scoreboard.scores == {}


@pytest.mark.parametrize(
    ("operation_ids", "max_n", "question_count", "message"),
    [
        ([], None, None, "A drill needs operation ids"),
        (
            ["add"],
            1,
            None,
            r"max_n 1 is too small for operation ids \['add'\]\. Give 2",
        ),
        (
            ["multiplication", "subtract"],
            1,
            None,
            r"max_n 1 is too small for operation ids \['subtract'\]\. Give 2",
        ),
        (["multiplication"], 0, None, r"operation ids \['multiplication'\]\. Give 1"),
        (["add"], None, 0, "question_count 0 is below 1"),
    ],
)
def test_drill__rejects(
    operation_ids: list[str],
    max_n: int | None,
    question_count: int | None,
    message: str,
) -> None:
    """A drill with no operations, too small a largest number or no questions fails."""
    with pytest.raises(ValueError, match=message):
        Drill(operation_ids, max_n=max_n, question_count=question_count)


def test_drill__smallest_max_n() -> None:
    """Multiplication and division accept 1 as the largest number."""
    # When
    drill = Drill(["multiplication", "division"], max_n=1)

    # Then
    assert drill.max_n == 1


@pytest.mark.parametrize(("question_count", "asked"), [(2, 2), (None, 50)])
def test_questions(
    monkeypatch: pytest.MonkeyPatch, question_count: int | None, asked: int
) -> None:
    """A drill asks ``question_count`` questions, or never stops without one."""
    # Given
    monkeypatch.setattr("tabliczka.practice.service.choice", lambda operations: ADD)
    questions = Drill(["add"], question_count=question_count).questions()

    # When
    taken = [question for question, _ in zip(questions, range(50), strict=False)]

    # Then
    assert len(taken) == asked


@pytest.mark.parametrize(
    ("max_n", "upper_bounds"),
    [(None, [20, 10]), (7, [7, 7])],
)
def test_questions__max_n(
    monkeypatch: pytest.MonkeyPatch, max_n: int | None, upper_bounds: list[int]
) -> None:
    """Each operation uses ``max_n`` when given and its own default otherwise."""
    # Given
    operations = iter((ADD, MULTIPLY))
    monkeypatch.setattr(
        "tabliczka.practice.service.choice", lambda choices: next(operations)
    )
    asked_upper_bounds: list[int] = []

    def randint(low: int, high: int) -> int:
        asked_upper_bounds.append(high)
        return low

    monkeypatch.setattr("tabliczka.exercises.service.randint", randint)
    drill = Drill(["add", "multiplication"], max_n=max_n, question_count=2)

    # When
    list(drill.questions())

    # Then
    assert [asked_upper_bounds[0], asked_upper_bounds[2]] == upper_bounds


@pytest.mark.parametrize(
    ("offset", "correct", "score"),
    [(0, True, Score(correct=1)), (1, False, Score(wrong=1))],
)
def test_check_answer(offset: int, *, correct: bool, score: Score) -> None:
    """An answer is checked against the question and counted for its operation."""
    # Given
    drill = Drill(["add"])
    question = ADD.generate(10)
    given = question.answer + offset

    # When
    result = drill.check_answer(question, given)

    # Then
    assert result is correct
    assert drill.scoreboard.score("add") == score


def test_summary() -> None:
    """The summary sums the drill's scores and lists each operation's, in order."""
    # Given
    drill = Drill(["subtract", "add", "division"])
    drill.scoreboard.record("add", correct=True)
    drill.scoreboard.record("add", correct=False)
    drill.scoreboard.record("subtract", correct=False)
    drill.scoreboard.record("multiplication", correct=True)

    # When
    summary = drill.summary()

    # Then
    assert summary == Summary(
        total=Score(correct=1, wrong=2),
        scores={
            "subtract": Score(wrong=1),
            "add": Score(correct=1, wrong=1),
            "division": Score(),
        },
    )
    assert list(summary.scores) == ["subtract", "add", "division"]
