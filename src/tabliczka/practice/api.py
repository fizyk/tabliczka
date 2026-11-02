"""Running a drill."""

from collections.abc import Sequence

from tabliczka.exercises.api import get_operations
from tabliczka.practice import service


def run_drill(
    operation_ids: Sequence[str],
    *,
    max_n: int | None = None,
    question_count: int | None = None,
) -> None:
    """Drill the operations with the given ids, then print the summary."""
    service.run_drill(
        get_operations(operation_ids), max_n=max_n, question_count=question_count
    )
