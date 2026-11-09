"""Keeping the learner's profile between runs of the program."""

from tabliczka.profiles import service
from tabliczka.profiles.models import Profile


def load_profile() -> Profile:
    """Return the profile saved for this user account, or an empty one when none is."""
    return service.load_profile()


def save_profile(profile: Profile) -> None:
    """Save the profile for this user account, replacing the one saved before."""
    service.save_profile(profile)
