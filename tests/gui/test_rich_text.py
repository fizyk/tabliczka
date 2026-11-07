"""Tests for the feedback and the summary as rich text."""

import pytest

from tabliczka.exercises.models import Question
from tabliczka.practice.models import Score, Summary
from tabliczka.ui.gui.rich_text import feedback_html, summary_html


@pytest.mark.parametrize(
    ("correct", "html"),
    [
        (True, '<span style="color: green">Dobrze!</span>'),
        (
            False,
            '<span style="color: red">Niestety, źle, prawidłowy wynik to 2.</span>',
        ),
    ],
)
def test_feedback_html(*, correct: bool, html: str) -> None:
    """A correct answer is praised in green, a wrong one corrected in red."""
    # Given
    question = Question(expression="1+1", answer=2, operation_id="add")

    # When / Then
    assert feedback_html(question, correct=correct) == html


def test_summary_html() -> None:
    """The summary shows the totals, then each operation's own score."""
    # Given
    summary = Summary(
        total=Score(correct=2, wrong=1),
        scores={"add": Score(correct=2), "subtract": Score(wrong=1)},
    )

    # When
    html = summary_html(summary)

    # Then
    assert html == (
        'Twój wynik to:<br><span style="color: green">2 - dobrze</span>'
        '<br><span style="color: red">1 - źle</span>'
        '<hr>Dodawanie:<br><span style="color: green">2 - dobrze</span>'
        '<hr>Odejmowanie:<br><span style="color: green">0 - dobrze</span>'
        '<br><span style="color: red">1 - źle</span>'
    )
