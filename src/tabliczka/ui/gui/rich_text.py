"""The feedback and the summary as coloured rich text, and the new version link."""

from html import escape

from tabliczka.exercises.models import Question
from tabliczka.practice.models import Score, Summary
from tabliczka.releases.models import Release
from tabliczka.ui.gui.text import NEW_VERSION_LINK_TEXT, NEW_VERSION_TEXT
from tabliczka.ui.text import (
    CORRECT_FEEDBACK,
    OPERATION_HEADINGS_BY_ID,
    SUMMARY_HEADING,
    correct_count,
    wrong_count,
    wrong_feedback,
)

CORRECT_COLOUR = "green"
WRONG_COLOUR = "red"


def coloured(text: str, colour: str) -> str:
    """Return the text as rich text in the colour."""
    return f'<span style="color: {colour}">{text}</span>'


def feedback_html(question: Question, *, correct: bool) -> str:
    """Return the feedback on an answer to the question, green when correct."""
    if correct:
        return coloured(CORRECT_FEEDBACK, CORRECT_COLOUR)
    return coloured(wrong_feedback(question), WRONG_COLOUR)


def summary_html(summary: Summary) -> str:
    """Return the totals, then the score of each operation, as rich text."""
    sections = [(SUMMARY_HEADING, summary.total)] + [
        (f"{OPERATION_HEADINGS_BY_ID[operation_id]}:", score)
        for operation_id, score in summary.scores.items()
    ]
    return "<hr>".join(
        "<br>".join([heading, *score_lines(score)]) for heading, score in sections
    )


def score_lines(score: Score) -> list[str]:
    """Return the correct count, then the wrong count when there are wrong answers."""
    lines = [coloured(correct_count(score), CORRECT_COLOUR)]
    if score.wrong:
        lines.append(coloured(wrong_count(score), WRONG_COLOUR))
    return lines


def new_version_html(release: Release) -> str:
    """Return the notice of a newer release, linking to its page."""
    notice = escape(NEW_VERSION_TEXT.format(version=release.version))
    return f'{notice} <a href="{escape(release.url)}">{NEW_VERSION_LINK_TEXT}</a>.'
