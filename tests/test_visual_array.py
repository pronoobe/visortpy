"""Unit tests for VisualArray operation recording accuracy."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from visortpy import VisualArray, OperationType


def test_read_recording():
    arr = VisualArray([10, 20, 30])
    _ = arr[0]
    assert len(arr.history) == 1
    rec = arr.history[0]
    assert rec.operation == OperationType.READ
    assert rec.indices == [0]
    assert rec.values == [10]


def test_write_recording():
    arr = VisualArray([10, 20, 30])
    arr[1] = 99
    assert len(arr.history) == 1
    rec = arr.history[0]
    assert rec.operation == OperationType.WRITE
    assert rec.indices == [1]
    assert rec.values == [99]
    assert rec.array_state == [10, 99, 30]


def test_swap_recording():
    arr = VisualArray([1, 2, 3])
    arr.swap(0, 2)
    assert len(arr.history) == 1
    rec = arr.history[0]
    assert rec.operation == OperationType.SWAP
    assert rec.indices == [0, 2]
    assert rec.values == [1, 3]
    assert rec.array_state == [3, 2, 1]


def test_compare_recording():
    arr = VisualArray([5, 3])
    result = arr.compare(0, 1)
    assert result == 1  # 5 > 3
    rec = arr.history[0]
    assert rec.operation == OperationType.COMPARE
    assert rec.meta["result"] == 1


def test_append_recording():
    arr = VisualArray([1, 2])
    arr.append(3)
    rec = arr.history[0]
    assert rec.operation == OperationType.WRITE
    assert rec.indices == [2]
    assert rec.array_state == [1, 2, 3]


def test_snapshot():
    arr = VisualArray([1, 2, 3])
    arr.snapshot()
    assert len(arr.history) == 1
    assert arr.history[0].meta.get("snapshot") is True


def test_context_manager():
    with VisualArray([5, 4, 3]) as arr:
        arr.swap(0, 2)
    # 2 snapshots (enter + exit) + 1 swap
    assert len(arr.history) == 3


def test_step_counter():
    arr = VisualArray([3, 1, 2])
    _ = arr[0]
    arr[1] = 10
    arr.swap(0, 2)
    steps = [r.step for r in arr.history]
    assert steps == [0, 1, 2]


def test_max_history_size():
    arr = VisualArray([1, 2, 3], max_history_size=2)
    _ = arr[0]
    _ = arr[1]
    _ = arr[2]
    assert len(arr.history) == 2
    assert arr.history[0].step == 1


def test_bubble_sort_correctness():
    arr = VisualArray([64, 34, 25, 12])
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr.swap(j, j + 1)
    assert arr.to_list() == [12, 25, 34, 64]
    assert len(arr.history) > 0


def test_repr_no_recording():
    arr = VisualArray([1, 2, 3])
    repr(arr)
    assert len(arr.history) == 0


def test_negative_index():
    arr = VisualArray([10, 20, 30])
    val = arr[-1]
    assert val == 30
    assert arr.history[0].indices == [2]


def test_len_and_iter():
    arr = VisualArray([1, 2, 3])
    assert len(arr) == 3
    assert list(arr) == [1, 2, 3]
    assert 2 in arr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
