"""Write the licence notices of Python and the libraries bundled into tabliczka.exe.

Run in the locked environment the program is built from, so the versions and
notices match what PyInstaller bundles:

    uv run --locked --group windows python release/notices.py dist/NOTICES.txt
"""

import os
import platform
import sys
from collections.abc import Iterator
from importlib.metadata import Distribution, distribution
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from PySide6.QtCore import qVersion

PROGRAM_NAME = "tabliczka"
QT_FOR_PYTHON_NAMES = {"pyside6-essentials", "shiboken6"}
LGPL_TEXT_PATH = Path(__file__).with_name("LGPL-3.0.txt")


def bundled_distributions(name: str) -> Iterator[Distribution]:
    """Yield the installed distributions the named one needs at run time."""
    seen = {canonicalize_name(name)}
    waiting = [name]
    while waiting:
        requirements = distribution(waiting.pop()).requires or []
        for requirement in map(Requirement, requirements):
            needed_name = canonicalize_name(requirement.name)
            if needed_name in seen:
                continue
            if requirement.marker and not requirement.marker.evaluate({"extra": ""}):
                continue
            seen.add(needed_name)
            waiting.append(needed_name)
            yield distribution(needed_name)


def licence_texts(bundled: Distribution) -> list[str]:
    """Return the texts of the licence files the distribution ships."""
    texts = []
    for licence_file in bundled.metadata.get_all("License-File") or []:
        text = bundled.read_text(f"licenses/{licence_file}")
        if text is None:
            text = bundled.read_text(licence_file)
        if text is None:
            raise SystemExit(
                f"{bundled.name} {bundled.version} declares the licence file "
                f"{licence_file} but does not ship it; "
                "add its licence text to release/ and to this script."
            )
        texts.append(text.strip())
    if not texts:
        raise SystemExit(
            f"{bundled.name} {bundled.version} ships no licence file; "
            "add its licence text to release/ and to this script."
        )
    return texts


def python_notice() -> str:
    """Return the licence notice of the Python interpreter running this script."""
    standard_library = Path(os.__file__).parent
    for folder in (standard_library, standard_library.parent):
        licence_path = folder / "LICENSE.txt"
        if licence_path.is_file():
            title = heading(f"Python {platform.python_version()} (PSF-2.0)")
            return f"{title}\n\n{licence_path.read_text(encoding='utf-8').strip()}"
    raise SystemExit(
        f"Python {platform.python_version()} ships no LICENSE.txt beside "
        f"{standard_library}; build with a Python that does."
    )


def heading(title: str) -> str:
    """Return the title underlined, as a section heading."""
    return f"{title}\n{'=' * len(title)}"


def qt_for_python_notice(program_version: str, pyside_version: str) -> str:
    """Return the notice for Qt for Python, with links to its source code."""
    qt_version = qVersion()
    return f"""{heading("Qt for Python")}

{PROGRAM_NAME} uses Qt for Python (PySide6 and Shiboken6 {pyside_version})
and Qt {qt_version} under the GNU Lesser General Public License, version 3
(LGPLv3), whose text closes this file. Their source code:

  PySide6 and Shiboken6:
  https://code.qt.io/cgit/pyside/pyside-setup.git/tag/?h=v{pyside_version}
  Qt:
  https://code.qt.io/cgit/qt/qt5.git/tag/?h=v{qt_version}

To build {PROGRAM_NAME} with a modified Qt, take its own source code from
https://github.com/fizyk/tabliczka/releases/tag/v{program_version}"""


def package_notice(bundled: Distribution) -> str:
    """Return the licence notice of one bundled Python package."""
    licence = bundled.metadata["License-Expression"] or bundled.metadata["License"]
    title = heading(f"{bundled.name} {bundled.version} ({licence})")
    return "\n\n".join([title, *licence_texts(bundled)])


def notices() -> str:
    """Return the notices of every library bundled into the program."""
    program_version = distribution(PROGRAM_NAME).version
    bundled = sorted(
        bundled_distributions(PROGRAM_NAME),
        key=lambda found: canonicalize_name(found.name),
    )
    qt_for_python = [
        found
        for found in bundled
        if canonicalize_name(found.name) in QT_FOR_PYTHON_NAMES
    ]
    qt_for_python_names = {canonicalize_name(found.name) for found in qt_for_python}
    if qt_for_python_names != QT_FOR_PYTHON_NAMES:
        raise SystemExit(
            f"{PROGRAM_NAME} no longer bundles all of {sorted(QT_FOR_PYTHON_NAMES)}; "
            "update QT_FOR_PYTHON_NAMES and the Qt for Python notice."
        )
    pyside_versions = {found.version for found in qt_for_python}
    if len(pyside_versions) != 1:
        raise SystemExit(
            f"PySide6 and Shiboken6 differ in version: {sorted(pyside_versions)}; "
            "lock them to the same version."
        )
    sections = [
        f"{PROGRAM_NAME} {program_version} is licensed under the GNU General Public "
        "License,\nversion 3 or later, in LICENSE.txt beside this file. "
        "It bundles Python and the\nlibraries below, each under its own licence.",
        python_notice(),
        qt_for_python_notice(program_version, pyside_versions.pop()),
        *(package_notice(found) for found in bundled if found not in qt_for_python),
        heading("GNU Lesser General Public License, version 3"),
        LGPL_TEXT_PATH.read_text(encoding="utf-8").strip(),
    ]
    return "\n\n\n".join(sections) + "\n"


def main() -> None:
    """Write the notices to the path given as the only argument."""
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python release/notices.py <output path>")
    Path(sys.argv[1]).write_text(notices(), encoding="utf-8")


if __name__ == "__main__":
    main()
