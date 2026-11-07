"""The page that shows a drill's summary."""

from PySide6.QtWidgets import QLabel

from tabliczka.practice.models import Summary
from tabliczka.ui.gui.rich_text import summary_html


class SummaryPage(QLabel):
    """Shows a drill's summary."""

    def __init__(self, summary: Summary) -> None:
        """Show the totals, then the score of each operation."""
        super().__init__(summary_html(summary))
