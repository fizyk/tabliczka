"""Reading and writing a profile as a JSON file."""

import json
from dataclasses import asdict
from pathlib import Path
from tempfile import NamedTemporaryFile

from tabliczka.profiles.models import Profile


def read(path: Path) -> Profile | None:
    """Return the profile stored at ``path``, or ``None`` when there is no file."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    fields = json.loads(text)
    fields["operation_ids"] = tuple(fields["operation_ids"])
    return Profile(**fields)


def write(path: Path, profile: Profile) -> None:
    """Store the profile at ``path``, creating its folder when missing.

    An interrupted write leaves the file stored before intact.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete_on_close=False
    ) as temporary_file:
        temporary_file.write(json.dumps(asdict(profile), ensure_ascii=False))
        temporary_file.close()
        Path(temporary_file.name).replace(path)
