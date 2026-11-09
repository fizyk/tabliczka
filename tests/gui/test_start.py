"""Tests for the start page."""

import pytest
from pytestqt.qtbot import QtBot

from tabliczka.profiles.models import Profile
from tabliczka.ui.gui.pages.start import StartPage

EMPTY_PROFILE = Profile(
    "",
    ("add", "subtract", "multiplication", "division"),
    max_n=None,
    question_count=None,
)


def choose(page: StartPage, name: str, operation_ids: list[str]) -> None:
    """Type the name and choose only the operations with the given ids."""
    page.name.setText(name)
    for operation_id, box in page.operation_boxes.items():
        box.setChecked(operation_id in operation_ids)


@pytest.mark.parametrize(
    ("name", "operation_ids", "enabled"),
    [
        ("Ala", ["add"], True),
        ("  ", ["add"], False),
        ("Ala", [], False),
    ],
)
def test_start_page__start_button(
    qtbot: QtBot,
    name: str,
    operation_ids: list[str],
    *,
    enabled: bool,
) -> None:
    """The drill starts only with a name and at least one operation."""
    # Given
    page = StartPage(EMPTY_PROFILE)
    qtbot.addWidget(page)

    # When
    choose(page, name, operation_ids)

    # Then
    assert page.start_button.isEnabled() is enabled


@pytest.mark.parametrize(
    ("operation_ids", "minimum"),
    [(["add", "subtract"], 1), (["multiplication", "division"], 0), ([], 0)],
)
def test_start_page__largest_number_default(
    qtbot: QtBot, operation_ids: list[str], minimum: int
) -> None:
    """The largest number stays each operation's own until chosen."""
    # Given
    page = StartPage(EMPTY_PROFILE)
    qtbot.addWidget(page)

    # When
    choose(page, "Ala", operation_ids)

    # Then
    assert page.max_n.minimum() == minimum
    assert page.max_n.text() == "jak zwykle"
    assert page.chosen_max_n() is None


@pytest.mark.parametrize(("chosen", "max_n"), [(1, 2), (5, 5)])
def test_start_page__largest_number_chosen(
    qtbot: QtBot, chosen: int, max_n: int
) -> None:
    """A chosen largest number stays chosen, raised to what the operations allow."""
    # Given
    page = StartPage(EMPTY_PROFILE)
    qtbot.addWidget(page)
    choose(page, "Ala", ["multiplication"])
    page.max_n.setValue(chosen)

    # When
    page.operation_boxes["add"].setChecked(True)

    # Then
    assert page.chosen_max_n() == max_n


@pytest.mark.parametrize(
    ("max_n", "question_count", "profile"),
    [
        (12, 5, Profile("Ala", ("add", "division"), max_n=12, question_count=5)),
        (
            0,
            0,
            Profile("Ala", ("add", "division"), max_n=None, question_count=None),
        ),
    ],
)
def test_start_page__profile(
    qtbot: QtBot, max_n: int, question_count: int, profile: Profile
) -> None:
    """The typed name and the chosen operations and limits are returned together."""
    # Given
    page = StartPage(EMPTY_PROFILE)
    qtbot.addWidget(page)
    choose(page, " Ala ", ["division", "add"])
    page.max_n.setValue(max_n)
    page.question_count.setValue(question_count)

    # When / Then
    assert page.profile() == profile


@pytest.mark.parametrize(
    "profile",
    [
        Profile("Ala", ("add", "division"), max_n=12, question_count=5),
        Profile("Ala", ("multiplication",), max_n=None, question_count=None),
    ],
)
def test_start_page__shows_profile(qtbot: QtBot, profile: Profile) -> None:
    """A page built from a profile returns it unchanged."""
    # When
    qtbot.addWidget(page := StartPage(profile))

    # Then
    assert page.profile() == profile
    assert page.start_button.isEnabled()
