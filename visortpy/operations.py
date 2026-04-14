"""Standard operation types and record structure for VisualArray history."""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class OperationType(Enum):
    """Types of operations that VisualArray can record."""
    COMPARE = "compare"
    READ = "read"
    WRITE = "write"
    SWAP = "swap"


@dataclass
class OperationRecord:
    """A single recorded operation in the VisualArray history.

    Attributes:
        step: Sequential step number.
        operation: The type of operation performed.
        indices: List of array indices involved.
        values: List of values involved.
        array_state: Full snapshot of the array after this operation.
        meta: Optional metadata (e.g. comparison result).
    """
    step: int
    operation: OperationType
    indices: List[int]
    values: List[Any]
    array_state: List[Any]
    meta: Optional[Dict[str, Any]] = field(default_factory=dict)

    def _asdict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        d = asdict(self)
        d["operation"] = self.operation.value
        return d
