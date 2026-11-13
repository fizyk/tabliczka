"""One published version of the program."""

from dataclasses import dataclass

from packaging.version import Version


@dataclass(frozen=True)
class Release:
    """A published version of the program and the page it is published on."""

    version: Version
    page_url: str
