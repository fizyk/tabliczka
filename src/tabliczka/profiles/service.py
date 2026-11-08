"""Keeping the profile in the user account's app data folder."""

from pathlib import Path

from platformdirs import user_config_dir

from tabliczka.exercises.api import get_operations
from tabliczka.profiles import repository
from tabliczka.profiles.models import Profile

APPLICATION_NAME = "tabliczka"
PROFILE_FILE_NAME = "profile.json"


def profile_path() -> Path:
    """Return the path of the profile file in the user account's app data folder."""
    return Path(
        user_config_dir(APPLICATION_NAME, appauthor=False, roaming=True)
    ).joinpath(PROFILE_FILE_NAME)


def load_profile() -> Profile | None:
    """Return the saved profile, or ``None`` when none is saved.

    Reject a profile file that cannot be read back as a profile.
    """
    path = profile_path()
    try:
        profile = repository.read(path)
        if profile is not None:
            get_operations(profile.operation_ids)
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(
            f"The profile file {path} cannot be read ({error!r}). "
            "Delete it to start with no saved profile."
        ) from error
    return profile


def save_profile(profile: Profile) -> None:
    """Save the profile, replacing the one saved before."""
    repository.write(profile_path(), profile)
