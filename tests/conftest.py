"""Settings shared by the tests."""

import os
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(autouse=True)
def app_data_folder(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Keep the saved profile in a temporary folder, not the user account's."""
    folder = tmp_path / "app-data"
    monkeypatch.setattr(
        "tabliczka.profiles.service.user_config_dir",
        lambda application_name, *, appauthor, roaming: str(folder),
    )
    return folder
