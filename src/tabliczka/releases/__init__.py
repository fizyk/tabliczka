"""The program's releases on GitHub, and whether a newer one is out."""

from tabliczka.releases.service import LATEST_RELEASE_URL, is_newer, read_release

__all__ = ["LATEST_RELEASE_URL", "is_newer", "read_release"]
