"""Keeping the profile in the user account's app data folder."""

from pathlib import Path

from platformdirs import user_config_dir

from tabliczka.core.constants import APPLICATION_NAME
from tabliczka.exercises import get_operations
from tabliczka.profiles.models import Profile
from tabliczka.profiles.repository import ProfileRepository

PROFILE_FILE_NAME = "profile.json"


def profile_path() -> Path:
    """Return the path of the profile file in the user account's app data folder."""
    return Path(
        user_config_dir(APPLICATION_NAME, appauthor=False, roaming=True)
    ).joinpath(PROFILE_FILE_NAME)


def check_field_types(profile: Profile) -> None:
    """Reject a profile whose fields do not hold the types ``Profile`` declares."""
    limits_valid = all(
        limit is None or type(limit) is int
        for limit in (profile.largest_number, profile.question_count)
    )
    if not isinstance(profile.name, str) or not limits_valid:
        raise ValueError(
            "A profile needs a name as text, "
            "and largest_number and question_count as whole numbers or null."
        )


def load_profile() -> Profile:
    """Return the saved profile, or an empty one when none is saved.

    Reject a profile file that cannot be read back as a profile.
    """
    path = profile_path()
    try:
        profile = ProfileRepository(path).read()
        check_field_types(profile)
        get_operations(profile.operation_ids)
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(
            f"The profile file {path} cannot be read ({error!r}). "
            "Delete it to start with no saved profile."
        ) from error
    return profile


def save_profile(profile: Profile) -> None:
    """Save the profile, replacing the one saved before."""
    ProfileRepository(profile_path()).write(profile)
