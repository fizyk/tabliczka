"""Finding the operations a drill can use."""

from collections.abc import Sequence

from tabliczka.exercises.models import Operation
from tabliczka.exercises.service import OPERATIONS_BY_ID


def get_operations(operation_ids: Sequence[str]) -> list[Operation]:
    """Return the operations with the given ids, in the same order."""
    unknown = set(operation_ids) - OPERATIONS_BY_ID.keys()
    if unknown:
        raise ValueError(
            f"Unknown operation ids {sorted(unknown)}. "
            f"Use ids from {list(OPERATIONS_BY_ID)}."
        )
    return [OPERATIONS_BY_ID[operation_id] for operation_id in operation_ids]
