"""Reading and writing a profile as a JSON file."""

import json
from dataclasses import asdict
from pathlib import Path
from tempfile import NamedTemporaryFile

from tabliczka.profiles.models import Profile


class ProfileRepository:
    """A profile stored as a JSON file at one path."""

    def __init__(self, path: Path) -> None:
        """Use the file at ``path``."""
        self.path = path

    def read(self) -> Profile:
        """Return the stored profile, or an empty one when there is no file."""
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return Profile(
                name="", operation_ids=(), largest_number=None, question_count=None
            )
        fields = json.loads(text)
        fields["operation_ids"] = tuple(fields["operation_ids"])
        return Profile(**fields)

    def write(self, profile: Profile) -> None:
        """Store the profile, creating its folder when missing.

        An interrupted write leaves the file stored before intact.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=self.path.parent, delete_on_close=False
        ) as temporary_file:
            temporary_file.write(json.dumps(asdict(profile), ensure_ascii=False))
            temporary_file.close()
            Path(temporary_file.name).replace(self.path)
