"""Run the tabliczka command line with ``python -m tabliczka`` or as a Windows program.

The Windows program runs in a console window that closes when the program ends, so
it waits for a key press first, keeping the summary readable.
"""

import sys

import click

from tabliczka.cli import main

if __name__ == "__main__":
    try:
        main()
    finally:
        if getattr(sys, "frozen", False):
            click.pause("Naciśnij dowolny klawisz, żeby zamknąć okno.")
