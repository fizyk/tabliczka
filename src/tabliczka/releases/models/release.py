"""One published version of the program."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Release:
    """A published version of the program and the page it is published on.

    ``version`` has no leading ``v``, such as ``0.5.0``.
    """

    version: str
    url: str
