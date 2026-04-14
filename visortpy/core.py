"""VisualArray — a list wrapper that records all mutations as operation history."""

from __future__ import annotations

import copy
from typing import Any, Dict, Iterable, Iterator, List, Optional, overload

from .operations import OperationRecord, OperationType


class VisualArray:
    """A list wrapper that transparently records every access and mutation.

    Usage::

        arr = VisualArray([64, 34, 25, 12])
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr.swap(j, j + 1)
        # arr.history now contains the full operation trace
    """

    def __init__(
        self,
        data: Iterable[Any] | None = None,
        *,
        max_history_size: Optional[int] = None,
    ) -> None:
        self._data: List[Any] = list(data) if data is not None else []
        self._history: List[OperationRecord] = []
        self._step: int = 0
        self._recording: bool = True
        self._max_history_size: Optional[int] = max_history_size

    # -- context manager --

    def __enter__(self) -> "VisualArray":
        self.snapshot()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.snapshot()

    # -- history access --

    @property
    def history(self) -> List[OperationRecord]:
        return list(self._history)

    # -- recording helpers --

    def _record(
        self,
        op: OperationType,
        indices: List[int],
        values: List[Any],
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        if not self._recording:
            return
        record = OperationRecord(
            step=self._step,
            operation=op,
            indices=indices,
            values=values,
            array_state=self._snapshot_data(),
            meta=meta or {},
        )
        self._history.append(record)
        self._step += 1
        if self._max_history_size and len(self._history) > self._max_history_size:
            self._history.pop(0)

    def _snapshot_data(self) -> List[Any]:
        return copy.deepcopy(self._data)

    def snapshot(self) -> None:
        """Manually record a full state snapshot (e.g. start/end marker)."""
        self._record(OperationType.READ, [], [], meta={"snapshot": True})

    # -- list-like interface --

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._data)

    def __contains__(self, item: Any) -> bool:
        return item in self._data

    @overload
    def __getitem__(self, index: int) -> Any: ...
    @overload
    def __getitem__(self, index: slice) -> List[Any]: ...

    def __getitem__(self, index: Any) -> Any:
        value = self._data[index]
        if isinstance(index, int):
            idx = index if index >= 0 else len(self._data) + index
            self._record(OperationType.READ, [idx], [value])
        return value

    def __setitem__(self, index: int, value: Any) -> None:
        if isinstance(index, int):
            idx = index if index >= 0 else len(self._data) + index
            self._data[index] = value
            self._record(OperationType.WRITE, [idx], [value])
        else:
            self._data[index] = value

    def __gt__(self, other: Any) -> bool:
        raise TypeError("Compare elements, not the array itself")

    def __lt__(self, other: Any) -> bool:
        raise TypeError("Compare elements, not the array itself")

    # -- explicit operations --

    def swap(self, i: int, j: int) -> None:
        """Swap elements at indices *i* and *j*, recorded as a single SWAP."""
        self._recording = False
        vi, vj = self._data[i], self._data[j]
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._recording = True
        self._record(OperationType.SWAP, [i, j], [vi, vj])

    def compare(self, i: int, j: int) -> int:
        """Compare elements at *i* and *j*. Returns -1, 0, or 1."""
        vi, vj = self._data[i], self._data[j]
        result = (vi > vj) - (vi < vj)
        self._record(
            OperationType.COMPARE, [i, j], [vi, vj], meta={"result": result}
        )
        return result

    def append(self, value: Any) -> None:
        self._data.append(value)
        idx = len(self._data) - 1
        self._record(OperationType.WRITE, [idx], [value])

    def pop(self, index: int = -1) -> Any:
        idx = index if index >= 0 else len(self._data) + index
        value = self._data.pop(index)
        self._record(OperationType.WRITE, [idx], [value], meta={"removed": True})
        return value

    # -- representation (no recording) --

    def __repr__(self) -> str:
        self._recording = False
        try:
            return f"VisualArray({self._data!r})"
        finally:
            self._recording = True

    def __str__(self) -> str:
        return self.__repr__()

    def to_list(self) -> List[Any]:
        """Return a plain list copy of the current data."""
        return list(self._data)
