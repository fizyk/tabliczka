"""Reading GitHub's latest release and comparing its version with the program's."""

import json
import re

from tabliczka.releases.models import Release

LATEST_RELEASE_URL = "https://api.github.com/repos/fizyk/tabliczka/releases/latest"
RELEASE_PAGES_URL = "https://github.com/fizyk/tabliczka/releases/"
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

    Reject a reply that does not name the release's tag and its page among the
    program's releases on GitHub.
    """
    fields = json.loads(reply_body)
    if not isinstance(fields, dict):
        raise ValueError(
            "GitHub's reply about the latest release is not "
            "a JavaScript Object Notation (JSON) object; "
            "check that LATEST_RELEASE_URL asks for the latest release."
        )
    tag = fields.get("tag_name")
    page_url = fields.get("html_url")
    if not isinstance(tag, str) or not isinstance(page_url, str):
        raise ValueError(
            "GitHub's reply about the latest release needs tag_name and html_url "
            "as text; check that LATEST_RELEASE_URL asks for the latest release."
        )
    version_numbers(tag)
    if not page_url.startswith(RELEASE_PAGES_URL):
        raise ValueError(
            f"The release page {page_url!r} is not under {RELEASE_PAGES_URL}; "
            "check that LATEST_RELEASE_URL asks for this program's latest release."
        )
    return Release(version=tag.removeprefix("v"), page_url=page_url)


def is_newer(release: Release, program_version: str) -> bool:
    """Return whether the release's version is later than ``program_version``."""
    return version_numbers(release.version) > version_numbers(program_version)
