"""Finding the operations a drill can use."""

from collections.abc import Sequence

from tabliczka.exercises import service
from tabliczka.exercises.models import Operation


def get_operation_ids() -> list[str]:
    """Return the id of every operation."""
    return service.get_operation_ids()


def get_operations(operation_ids: Sequence[str]) -> list[Operation]:
    """Return the operations with the given ids, in the same order."""
    return service.get_operations(operation_ids)
