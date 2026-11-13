"""Tests for reading the latest release and comparing its version."""

import pytest

from tabliczka.releases import is_newer, read_release
from tabliczka.releases.models import Release

RELEASE_PAGE = "https://github.com/fizyk/tabliczka/releases/tag/v0.5.0"


def test_read_release() -> None:
    """The reply's tag, without its ``v``, and page make the release."""
    # Given
    reply_body = (
        b'{"tag_name": "v0.5.0", "html_url": "' + RELEASE_PAGE.encode() + b'", '
        b'"name": "tabliczka 0.5.0"}'
    )

    # When
    release = read_release(reply_body)

    # Then
    assert release == Release(version="0.5.0", page_url=RELEASE_PAGE)


@pytest.mark.parametrize(
    ("reply_body", "message"),
    [
        (b"{", "Expecting"),
        (b"\xff", "utf-8"),
        (b"[]", "is not a JavaScript Object Notation"),
        (b'{"html_url": "https://github.example/"}', "tag_name and html_url"),
        (b'{"tag_name": "v0.5.0"}', "tag_name and html_url"),
        (b'{"tag_name": 5, "html_url": "https://github.example/"}', "tag_name"),
        (
            b'{"tag_name": "latest", "html_url": "https://github.example/"}',
            "three whole numbers",
        ),
        (
            b'{"tag_name": "v0.5.0-rc1", "html_url": "https://github.example/"}',
            "three whole numbers",
        ),
        (
            b'{"tag_name": "v0.5.0", "html_url": "file:///C:/Windows/notepad.exe"}',
            "is not under",
        ),
        (
            b'{"tag_name": "v0.5.0", "html_url": "http://github.com/fizyk/tabliczka/'
            b'releases/tag/v0.5.0"}',
            "is not under",
        ),
        (
            b'{"tag_name": "v0.5.0", "html_url": "https://github.example/fizyk/'
            b'tabliczka/releases/tag/v0.5.0"}',
            "is not under",
        ),
    ],
)
def test_read_release__rejects(reply_body: bytes, message: str) -> None:
    """A reply that does not name a release's version and page is rejected."""
    # When / Then
    with pytest.raises(ValueError, match=message):
        read_release(reply_body)


@pytest.mark.parametrize(
    ("version", "program_version", "newer"),
    [
        ("0.5.0", "0.4.1", True),
        ("0.4.2", "0.4.1", True),
        ("1.0.0", "0.10.0", True),
        ("0.10.0", "0.9.0", True),
        ("0.4.1", "0.4.1", False),
        ("0.4.0", "0.4.1", False),
        ("0.9.0", "0.10.0", False),
    ],
)
def test_is_newer(version: str, program_version: str, *, newer: bool) -> None:
    """Only a later version counts as newer, compared number by number."""
    # When / Then
    assert is_newer(Release(version, RELEASE_PAGE), program_version) is newer
