"""Reading GitHub's latest release and comparing its version with the program's."""

import json
import re

from tabliczka.releases.models import Release

LATEST_RELEASE_URL = "https://api.github.com/repos/fizyk/tabliczka/releases/latest"
VERSION_PATTERN = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")


def version_numbers(version: str) -> tuple[int, int, int]:
    """Return the major, minor and patch numbers of a version such as ``v0.5.0``."""
    match = VERSION_PATTERN.fullmatch(version)
    if match is None:
        raise ValueError(
            f"The version {version!r} is not three whole numbers joined by dots, "
            "such as 0.5.0; pass a version in that form."
        )
    major, minor, patch = (int(number) for number in match.groups())
    return major, minor, patch


def read_release(reply_body: bytes) -> Release:
    """Return the release described by GitHub's reply about the latest release.

    Reject a reply that does not name the release's tag and page.
    """
    fields = json.loads(reply_body)
    if not isinstance(fields, dict):
        raise ValueError("A release reply needs to be a JSON object.")
    tag = fields.get("tag_name")
    url = fields.get("html_url")
    if not isinstance(tag, str) or not isinstance(url, str):
        raise ValueError("A release reply needs tag_name and html_url as text.")
    version_numbers(tag)
    return Release(version=tag.removeprefix("v"), url=url)


def is_newer(release: Release, current_version: str) -> bool:
    """Return whether the release's version is later than ``current_version``."""
    return version_numbers(release.version) > version_numbers(current_version)
