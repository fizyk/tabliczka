"""Tests for keeping the learner's profile between runs."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tabliczka.profiles.api import load_profile, save_profile
from tabliczka.profiles.models import Profile


@pytest.mark.parametrize(
    "profile",
    [
        Profile("Ala", ("add", "division"), largest_number=12, question_count=5),
        Profile("Łucja", ("subtract",), largest_number=None, question_count=None),
    ],
)
def test_save_profile(app_data_folder: Path, profile: Profile) -> None:
    """A saved profile is loaded back from the app data folder."""
    # Given
    save_profile(Profile("Olek", ("add",), largest_number=None, question_count=None))

    # When
    save_profile(profile)

    # Then
    assert (app_data_folder / "profile.json").is_file()
    assert load_profile() == profile


def test_save_profile__interrupted(
    monkeypatch: pytest.MonkeyPatch, app_data_folder: Path
) -> None:
    """A save that does not finish leaves only the profile saved before."""
    # Given
    saved = Profile("Ala", ("add",), largest_number=None, question_count=None)
    save_profile(saved)
    monkeypatch.setattr(
        Path, "replace", MagicMock(spec=Path.replace, side_effect=OSError)
    )

    # When
    with pytest.raises(OSError):
        save_profile(
            Profile("Olek", ("add",), largest_number=None, question_count=None)
        )

    # Then
    assert load_profile() == saved
    assert [file.name for file in app_data_folder.iterdir()] == ["profile.json"]


def test_load_profile__empty() -> None:
    """Before the first save the profile has no name and no operations."""
    # When / Then
    assert load_profile() == Profile("", (), largest_number=None, question_count=None)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("{", "JSONDecodeError"),
        ("[]", "TypeError"),
        ('"text"', "TypeError"),
        ('{"name": "Ala"}', "KeyError"),
        (
            '{"name": "Ala", "operation_ids": ["add"], "largest_number": null}',
            "TypeError",
        ),
        (
            '{"name": "Ala", "operation_ids": ["power"], "largest_number": null, '
            '"question_count": null}',
            "Unknown operation ids",
        ),
        (
            '{"name": 12, "operation_ids": ["add"], "largest_number": null, '
            '"question_count": null}',
            "A profile needs",
        ),
        (
            '{"name": "Ala", "operation_ids": ["add"], "largest_number": "12", '
            '"question_count": null}',
            "A profile needs",
        ),
        (
            '{"name": "Ala", "operation_ids": ["add"], "largest_number": null, '
            '"question_count": 1.5}',
            "A profile needs",
        ),
    ],
)
def test_load_profile__rejects(
    app_data_folder: Path, content: str, message: str
) -> None:
    """A profile file that is not a profile is rejected, naming the file."""
    # Given
    app_data_folder.mkdir()
    (app_data_folder / "profile.json").write_text(content, encoding="utf-8")

    # When / Then
    with pytest.raises(ValueError, match="profile.json cannot be read") as error_info:
        load_profile()
    assert message in str(error_info.value)
