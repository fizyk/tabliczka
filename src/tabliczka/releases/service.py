"""Reading GitHub's latest release and comparing its version with the program's."""

import json

from packaging.version import Version

from tabliczka.releases.models import Release

LATEST_RELEASE_URL = "https://api.github.com/repos/fizyk/tabliczka/releases/latest"
RELEASE_PAGES_URL = "https://github.com/fizyk/tabliczka/releases/"


def read_release(reply_body: bytes) -> Release:
    """Return the release described by GitHub's reply about the latest release.

    Reject a reply that does not name the release's tag and its page among the
    program's releases on GitHub.
    """
    reply = json.loads(reply_body)
    if not isinstance(reply, dict):
        raise ValueError(
            "GitHub's reply about the latest release is not "
            "a JavaScript Object Notation (JSON) object; "
            "check that LATEST_RELEASE_URL asks for the latest release."
        )
    tag = reply.get("tag_name")
    page_url = reply.get("html_url")
    if not isinstance(tag, str) or not isinstance(page_url, str):
        raise ValueError(
            "GitHub's reply about the latest release needs tag_name and html_url "
            "as text; check that LATEST_RELEASE_URL asks for the latest release."
        )
    version = Version(tag)
    if not page_url.startswith(RELEASE_PAGES_URL):
        raise ValueError(
            f"The release page {page_url!r} is not under {RELEASE_PAGES_URL}; "
            "check that LATEST_RELEASE_URL asks for this program's latest release."
        )
    return Release(version=version, page_url=page_url)


def is_newer(release: Release, program_version: str) -> bool:
    """Return whether the release's version is later than ``program_version``."""
    return release.version > Version(program_version)
